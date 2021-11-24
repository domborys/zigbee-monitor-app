<template>
    <div class="dropdown-menu" @focusin="dropdownFocusIn" @focusout="dropdownFocusOut">
        <button type="button" class="header-button dropdown-toggle" @click="toggleDropdown">
            <slot name="toggle-button"></slot>
        </button>
        <div v-if="expanded" class="dropdown-content" @click="collapseDropdown">
            <slot name="content"></slot>
        </div>
    </div>
</template>

<script>
export default {
    name:"AppHeader",
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