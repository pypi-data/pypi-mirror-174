<script lang="ts">
    export let params: {
        noteContent?: string;
        noteTitle?: string;
        logs?: { [key: string]: string };
        filename?: string;
    };

    import NoteEditor from "../components/NoteEditor.svelte";
    import NoteHistory from "../components/NoteHistory.svelte";
    import RecordCard from "../components/RecordCard.svelte";
    import ContentOutline from "../components/ContentOutline.svelte";
    import { webSocket, sessionState, waitForOpenConnection } from "../stores";
    import type { Record } from "../types/record.type";
    import { onMount } from "svelte";
    import { createMemoryHistory } from "history";
    import { WrappedHistory } from "../utils/history";

    // Create own history instance.
    let history = new WrappedHistory(createMemoryHistory());

    let relevantRecords: Record[] = [];
    let connectedToBackend: boolean = false;
    let noteTitle: string = "";
    let noteContent: string = "";
    let headlines: string[] = [];
    let noteEditor: NoteEditor;
    let allContent: { [key: string]: string } = {};

    // this is only set first time when this component is rendered
    let originalNote = {
        filename: params.filename,
        scrollLocation: -1,
    };

    // to support clicked prompts history
    let clickedRecord: Record;
    let disabledBackButton = false;
    let disabledForwardButton = true;

    onMount(() => {
        sessionState.relevantRecords.subscribe((val) => {
            relevantRecords = val;
        });

        sessionState.connectedToBackend.subscribe((val) => {
            connectedToBackend = val;
        });
    });

    const getHeadlines = (content: string) => {
        if (content.length === 0) return [];
        let parser = new DOMParser();
        let htmlDoc = parser.parseFromString(content, "text/html");
        let allH2 = htmlDoc.getElementsByTagName("h2");
        let newHeadlines = [];
        for (const h2 of allH2) {
            newHeadlines.push(h2.textContent);
        }
        headlines = newHeadlines;
    };

    const onNoteSave = () => {
        if (webSocket === null) return;
        webSocket.send(
            JSON.stringify({
                type: "save_note",
            })
        );
    };

    const onNoteCancel = () => {
        if (webSocket === null) return;
        webSocket.send(
            JSON.stringify({
                type: "exit",
            })
        );
        setTimeout(window.close, 100);
    };

    const onNoteUpdate = (textContent: string, fullContent: string, updateType: string) => {
        if (webSocket === null) return;
        webSocket.send(JSON.stringify({
            "type": "update_note",
            "data": {
                "input": textContent,
                "content": fullContent,
                "updateType": updateType,
            }
        }));
    }

    const onImageUpload = (imgBase64: string) => {
        const imgData = imgBase64.split(",");
        webSocket.send(
            JSON.stringify({
                type: "upload_image",
                data: {
                    image: imgData[1],
                },
            })
        );
    };

    const onShowNote = (filename: string) => {
        if (webSocket === null) return;
        webSocket.send(
            JSON.stringify({
                type: "show_note",
                data: {
                    filename: filename,
                },
            })
        );
    };

    const onAbstractClose = (index: number) => {
        const func = () => {
            const pre_slice = relevantRecords.slice(0, index);
            const pos_slice = relevantRecords.slice(index + 1);
            relevantRecords = pre_slice.concat(pos_slice);
        };
        return func;
    };

    const onContentOutlineClick = (headlineIndex: number) => {
        let allH2 = [...document.getElementsByTagName("h2")];
        for (let [i, h2] of allH2.entries()) {
            if (i === headlineIndex) {
                window.scrollTo({
                    top: h2.offsetTop,
                    behavior: "smooth",
                });
            }
        }
    };

    const onPromptClick = (record: Record) => {
        if (record === clickedRecord) {
            return;
        }
        // switch the note content
        onShowNote(record.filename);
        // save the clicked record state
        clickedRecord = record;

        // save the state to self-managed history
        history.push("", record);

        // as user can go back and forward to different notes by clicking right side prompts, we need to save the first orignal note information to allow user to go back to very begining place
        if (originalNote.scrollLocation === -1) {
            originalNote = {
                ...originalNote,
                scrollLocation:
                    document.documentElement.scrollTop ||
                    document.body.scrollTop,
            };
        }
    };

    const goBack = () => {
        history.back();
    };

    const goForward = () => {
        history.forward();
    };

    $: {
        if (params.noteContent && noteContent !== params.noteContent) {
            // noteContent is changed from params, this means noteEditor needs to reset to a new content
            noteEditor?.resetContent(params.noteContent);
            getHeadlines(params.noteContent);
            noteContent = params.noteContent;
        }

        if (params.noteTitle && noteTitle !== params.noteTitle) {
            noteEditor?.resetTitle(params.noteTitle);
            noteTitle = params.noteTitle;
        }

        // evaluate the content history
        if (params.logs && allContent !== params.logs) {
            allContent = params.logs;
        }

        if (clickedRecord) {
            // need to scroll the window to the target tag location
            let allTargetTags = [
                ...document.getElementsByTagName(clickedRecord.headingType),
            ] as HTMLElement[];
            for (let [idx, element] of allTargetTags.entries()) {
                if (idx === clickedRecord.headingIdx) {
                    window.scrollTo({
                        top: element.offsetTop,
                        behavior: "smooth",
                    });
                }
            }
        } else if (originalNote.filename === params.filename) {
            // go back to orignal note's scroll location
            window.scrollTo({
                top: originalNote.scrollLocation,
                behavior: "smooth",
            });
        }

        // evaluate the forward/back button state
        disabledBackButton = !history.canBack();
        disabledForwardButton = !history.canForward();
    }

    history.listen(({ action, location }) => {
        // The current location changed.

        let record: Record | null = location.state as Record | null;
        if (record) {
            // switch the note content
            onShowNote(record.filename);
            // save the clicked record state
            clickedRecord = record;
        } else {
            // this might because user try to go back to the orignal note, thus load the orignal note and scroll to saved location
            onShowNote(originalNote.filename);
            // no record is clicked at this moment
            clickedRecord = undefined;
        }
    });
</script>

<div class="edit-note">
    <div class="fixed top-0 w-full h-8 pl-5 flex gap-4">
        <button
            class="disabled:opacity-40"
            disabled={disabledBackButton}
            on:click={goBack}
        >
            <box-icon class="" name="left-arrow-alt" />
        </button>
        <button
            class="disabled:opacity-40"
            disabled={disabledForwardButton}
            on:click={goForward}
        >
            <box-icon name="right-arrow-alt" />
        </button>
    </div>
    <div class="fixed top-8 bottom-0 left-0 w-16 ...">
        <ContentOutline {headlines} onClick={onContentOutlineClick} />
    </div>
    <div class="mt-8">
        <NoteEditor
            bind:this={noteEditor}
            onSave={onNoteSave}
            onCancel={onNoteCancel}
            onUpdate={onNoteUpdate}
            {onImageUpload}
            editable={connectedToBackend}
            title={noteTitle}
            content={noteContent}
            {getHeadlines}
        />
    </div>
    <div class="recordcards fixed top-8 right-0 bottom-0 overflow-y-auto">
        {#each relevantRecords as record, index}
            <RecordCard
                {record}
                onClose={onAbstractClose(index)}
                onClick={onPromptClick}
            />
        {/each}
    </div>

    {#key allContent}
        <NoteHistory content={allContent} />
    {/key}
</div>

<svelte:window on:load={async () => {
    if (!connectedToBackend) {
        if (webSocket === null || webSocket.readyState !== webSocket.OPEN) {
            try {
                await waitForOpenConnection(webSocket);
                webSocket.send(JSON.stringify({
                    "type": "exit"
                }));
            } catch (err) { console.error(err); }
        } else {
            webSocket.send(JSON.stringify({
                    "type": "exit"
            }));
        }
    }
}}/>

<style>
    @keyframes pop {
        0% {
            transform: scale(0.9);
            opacity: 0;
        }
        100% {
            transform: scale(1);
            opacity: 1;
        }
    }
    :global(.recordcards > *) {
        animation: pop 0.25s ease-out;

        /* hide scrollbar */
        -ms-overflow-style: none;
        overflow: -moz-scrollbars-none;
        scrollbar-width: none;
    }

    .recordcards::-webkit-scrollbar {
        display: none; /* Safari and Chrome */
    }
</style>
