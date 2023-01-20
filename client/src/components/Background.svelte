<!-- This is a component that fills its parent with an image,
which is sent as a prop. This component takes up no space in 
the DOM, but is used to set the background image of its parent.
When the image source changes, the background fades slowly out and in
with Svelte transitions. -->

<script>
    import { fade } from 'svelte/transition';
    export let background = "";
</script>

<div 
in:fade="{{ duration: 1000 }}" 
out:fade="{{ duration: 618 }}"
class="background" 
style="background-image: url({background});"
>
    <slot></slot>
</div>

<style>
    .background {
        width: 100%;
        height: 100%;
        background-size: cover;
        background-repeat: no-repeat;
        background-position: center;
        background-color: #4b3d00;
        position: absolute;
        top: 0;
        left: 0;
            }
</style>
