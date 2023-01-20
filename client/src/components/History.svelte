<script>
    import { fade } from 'svelte/transition';
    import Typewriter from 'svelte-typewriter';
    export let output
</script>

<!-- Display the output text. this will be scrollable with 
	the history of the game -->
<!-- <textarea bind:value={output} rows="10" cols="40"></textarea> -->
<!-- What I actually want is a full-width div that shows
text in a large font with a transparent backgrond. This text should 
scroll vertically but have a hidden scrollbar and only be a fixed height -->
<div transition:fade class="output">
    <Typewriter
        delay={100}
        interval={[1,1,2,3,5,8,13,21,34,55]}
    >
        {output}
    </Typewriter> 
</div>

<style>
    .output {
        text-align: left;
        text-shadow: 1px 1px 1px #4b3d00;
        color: #ffe466;
        font-size: 2rem;
        width: 100%;
        height: 100%;
        overflow-y: scroll;
        scrollbar-width: none;
    }
    /* Hide scrollbar for Chrome, Safari and Opera */
    .output::-webkit-scrollbar {
    display: none;
    }

    /* Hide scrollbar for IE, Edge and Firefox */
    .output {
    -ms-overflow-style: none;  /* IE and Edge */
    scrollbar-width: none;  /* Firefox */
    }
</style>