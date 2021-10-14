<template>
    <div class="dropdown-menu">
        <button type="button" class="header-button dropdown-toggle button-username" @click="toggleDropdown">
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
        }
    },
}
</script>


<style scoped>

</style>