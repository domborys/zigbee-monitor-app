<template>
    <div class="dropdown-menu" @focusin="dropdownFocusIn" @focusout="dropdownFocusOut">
        <button type="button" class="header-button dropdown-toggle" @click="toggleDropdown">
            <!-- @slot Contents of the button used for collapsing and expanding the menu. -->
            <slot name="toggle-button"></slot>
        </button>
        <div v-if="expanded" class="dropdown-content" @click="collapseDropdown">
            <!-- @slot The contents the dropdown menu.  -->
            <slot name="content"></slot>
        </div>
    </div>
</template>

<script>
/**
 * A dropdown menu intended to be used as a part of AppHeader.
 * The toggle-button is used for expanding and collapsing the contents.
 * The menu will be also collapsed when the user clicks inside the expanded menu
 * or when the menu loses focus (e.g. when user clicks outside the menu).
 */
export default {
    name:"DropdownMenu",
    data(){
        return{
            expanded:false
        }
    },
    methods:{
        toggleDropdown(){
            this.expanded = !this.expanded;
        },
        collapseDropdown(){
            this.expanded = false;
        },
        dropdownFocusIn(){
            if(this.focusOutTimer){
                clearTimeout(this.focusOutTimer);
            }
        },
        dropdownFocusOut(){
            this.focusOutTimer = setTimeout(() => {
                this.expanded = false;
            }, 0);
        },
    },
}
</script>


<style scoped>

</style>
