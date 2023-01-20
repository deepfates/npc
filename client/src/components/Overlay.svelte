<div class="overlay">
    <slot></slot>
</div>

<style>
    .overlay {
        box-shadow: inset 0 0 5em 1em #000;
        background-color: rgba(0, 0, 0, 0.2);
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        position: relative;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        padding: 0;
        margin: 0;
    }
</style>