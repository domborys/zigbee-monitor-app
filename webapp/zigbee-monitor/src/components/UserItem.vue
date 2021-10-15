<template>
    <li class="user-item">
        <h3 class="user-item-header" :class="{'header-disabled':user.disabled}">{{ user.username }}</h3>
        <div>
            {{ role }}
        </div>
    </li>
</template>

<script>

export default {
    name:"UserItem",
    props:{
        user: Object,
    },
    computed:{
        role(){
            const role = this.user.role === 'admin' ? 'Administrator' : 'Użytkownik';
            const state = this.user.disabled ? ' (zablokowany)' : '';
            return role + state;
        },
    },
    methods:{
    }
}
</script>


<style scoped>

.user-item{
    padding:10px;
    border-bottom: 1px solid #E6E6FA;
    border-right: 1px solid #E6E6FA;
    border-left: 1px solid #E6E6FA;
}

.user-item:first-child{
    border-top: 1px solid #E6E6FA;
}

.user-item:hover{
    background-color: #E6E6FA;
    cursor: pointer;
}

.user-item-header{
    margin:0 0 6px 0;
    font-size: 15px;
    font-weight:600;
}

.header-disabled{
    text-decoration: line-through;
}

</style>