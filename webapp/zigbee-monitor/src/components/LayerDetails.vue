<template>
    <section v-if="layer">
        <h2 class="layer-details-header">Informacje o warstwie</h2>
        <dl class="dl-inline details-list">
            <dt>Nazwa</dt>
            <dd>{{layer.name}}</dd>
            <dt>Szerokość</dt>
            <dd>{{layer.width}} m</dd>
            <dt>Wysokość</dt>
            <dd>{{layer.height}}</dd>
        </dl>
    </section>
</template>

<script>

export default {
    name:"LayerDetails",
    props:{
        layer: Object
    },
}
</script>


<style scoped>
.layer-details-header{
    font-size:22px;
    font-weight:bold;
}
.details-list dt{
    width:30%;
}

</style>