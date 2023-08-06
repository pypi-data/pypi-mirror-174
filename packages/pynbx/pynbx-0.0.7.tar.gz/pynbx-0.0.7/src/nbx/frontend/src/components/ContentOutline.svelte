<script lang="ts">
    export let headlines: string[];
    export let onClick: any;
</script>

<div class="drawer-side">
    <label for="my-drawer-2" class="drawer-overlay"></label>
    <ul class="menu p-4 overflow-y-auto w-80 bg-base-100 text-base-content">
      <!-- Sidebar content here -->
      {#if headlines.length > 0}
        <b>Table of content</b>
      {/if}
      {#each headlines as headline, index}
        <li><div on:click={onClick(index)}>{headline}</div></li>
      {/each}
    </ul>
</div>

<style>
</style>
