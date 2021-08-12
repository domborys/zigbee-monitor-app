<template>
    <div id="app">
        <main-layout/>
    </div>
</template>

<script>
import MainLayout from './components/MainLayout.vue'

export default {
    name: 'App',
    components: {
        MainLayout
    }
}
</script>

<style>
#app {
    width:100%;
    height:100%;
}
</style>
