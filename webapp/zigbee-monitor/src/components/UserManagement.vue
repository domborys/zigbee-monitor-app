<template>
    <div class="one-column-container user-management-container">
        <h2 class="user-list-header">Użytkownicy</h2>
        <button type="button" class="button" @click="addUser">Dodaj użytkownika</button>
        <ul class="user-list">
            <user-item v-for="user in users" :key="user.id" :user="user" @click.native="showUser(user)" />
        </ul>
        
        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce dapibus eleifend facilisis. Ut nec risus et quam rhoncus varius. Morbi eu tellus ac diam commodo ornare. Morbi ultrices velit neque, tempus mollis mauris pharetra pretium. Interdum et malesuada fames ac ante ipsum primis in faucibus. Sed non lacus semper, rhoncus velit nec, gravida nisl. Nulla pharetra risus quam, ut blandit sem finibus pulvinar. Nulla dictum tempus pellentesque. Maecenas efficitur felis gravida, tincidunt neque et, volutpat velit. Pellentesque nibh eros, fermentum vitae justo eget, faucibus auctor sem. Praesent porta mattis elit eget malesuada. Etiam pellentesque purus sed sapien condimentum, non dapibus ipsum bibendum. In id mattis massa, laoreet sodales tellus. Sed in cursus nibh. Proin laoreet elit eget rutrum iaculis. Sed enim felis, facilisis at tempus id, dictum luctus purus.

Integer consectetur sagittis est, et maximus nisl semper non. Proin egestas sem vitae molestie iaculis. Vivamus nulla augue, tincidunt ut consectetur et, tristique et lacus. Nulla id aliquet quam. Donec diam ligula, tincidunt vitae euismod vel, vehicula at nulla. Maecenas neque erat, malesuada eget leo eu, interdum dapibus nibh. Nullam malesuada nibh a odio congue, non ultrices justo pulvinar. Donec quis eros non nunc finibus rhoncus sed non ligula.

Aliquam venenatis vulputate nisl ut commodo. Maecenas orci justo, auctor a rutrum at, feugiat sit amet libero. Donec ut ex eu sapien placerat fermentum at et nunc. Aliquam varius, arcu eget ullamcorper blandit, risus massa bibendum turpis, vel bibendum turpis quam dictum urna. Praesent sapien justo, vestibulum eu metus ac, mollis venenatis lacus. Fusce tellus orci, semper ut risus eu, semper condimentum lorem. Mauris tempor velit dolor, eget iaculis augue cursus in.

Phasellus egestas libero sit amet consectetur fermentum. Quisque vestibulum et augue sed blandit. Mauris ultricies rhoncus tortor ut maximus. Sed vulputate, dolor in vestibulum dictum, justo quam varius elit, nec rutrum sem urna eget nibh. Integer magna nulla, fermentum sed malesuada rhoncus, posuere nec felis. Phasellus rhoncus, felis sed congue tincidunt, est nisl feugiat dui, id luctus sem leo sit amet enim. Phasellus posuere eleifend dapibus. Suspendisse consectetur quam ipsum, quis mollis lectus rutrum nec.

Etiam malesuada condimentum mi ut laoreet. Nunc quis velit orci. Aliquam erat volutpat. Duis at faucibus purus. Aliquam erat volutpat. Ut eu mauris imperdiet, imperdiet turpis et, tristique quam. Duis eu facilisis ex. Curabitur et velit porttitor, facilisis dolor et, ornare ipsum. Nunc ultrices nunc ut lacus mollis, vel vestibulum dolor lacinia. Suspendisse vitae tincidunt nunc, non aliquam erat. Morbi sit amet dictum nisl, viverra facilisis felis. Phasellus et ipsum pretium, luctus nisl sed, suscipit leo. Sed sapien neque, egestas ac laoreet sit amet, suscipit a ex. Phasellus ac orci dolor. Nam vitae lorem vel dui sagittis molestie.

Mauris blandit elit non rutrum vulputate. Curabitur rutrum orci nec est faucibus, in porta augue viverra. Fusce ut sapien sed dolor convallis faucibus eget eu tellus. Vestibulum eu malesuada sem, nec faucibus libero. Fusce vel arcu suscipit, ultricies mauris sit amet, imperdiet sapien. Suspendisse potenti. Sed in consectetur quam, quis cursus orci. Fusce vel ornare diam. Aenean suscipit ante ut mi aliquet, eu tincidunt lorem eleifend. Nullam placerat viverra ligula, sed imperdiet sapien mollis eu. Fusce tristique purus sapien, vitae aliquam mi venenatis id. Nulla facilisi.

In accumsan risus ac arcu sodales, in pulvinar lacus faucibus. Sed ac malesuada tellus, vel hendrerit arcu. Curabitur id scelerisque velit. Suspendisse posuere nulla luctus ex elementum, vel porta turpis malesuada. Maecenas auctor faucibus odio, sit amet dignissim nunc facilisis vel. Donec dignissim hendrerit tellus non ultrices. Donec elementum aliquam auctor. Sed ut mattis ex. Pellentesque sit amet ornare lectus. Phasellus quis nisl eu ligula fermentum tempor. Pellentesque nec blandit risus. Nam viverra, magna vel euismod ultrices, mi turpis laoreet augue, at pretium lectus dolor sit amet est. Aliquam a porttitor turpis, quis semper sapien. Ut sed faucibus orci, et suscipit urna. Sed varius libero sed enim consectetur, ut aliquet metus ullamcorper.

Pellentesque risus mi, consectetur eget pellentesque eu, consectetur in augue. Proin efficitur bibendum porta. Phasellus in vestibulum lacus, vel rutrum massa. Proin aliquet ligula est, vel porttitor tortor feugiat at. Mauris tincidunt lectus non purus condimentum varius. Vestibulum eget lectus et nulla hendrerit imperdiet sed sit amet nibh. Donec ultricies massa quis tellus finibus, non ultrices tortor pulvinar. Donec aliquam arcu venenatis velit commodo facilisis in sed odio. Morbi ullamcorper ipsum a ex eleifend pharetra. Curabitur interdum tincidunt convallis. Suspendisse quis enim sed tortor pellentesque commodo sed sit amet mi.

Nunc tempus fringilla malesuada. Aenean ullamcorper iaculis sem, ut lacinia lectus luctus eu. Cras nec fringilla ex. Aliquam quis ex sit amet mi dapibus porttitor at at nibh. Nulla finibus suscipit mauris vitae imperdiet. Morbi luctus ultrices leo, id aliquam massa molestie sed. Donec eget semper libero, in dictum mauris.
    </div>
</template>

<script>
import UserItem from './UserItem.vue'

export default {
    name:"UserManagement",
    components:{
        UserItem
    },
    props:{
    },
    computed:{
        users(){
            return this.$store.state.users.users;
        }
    },
    methods:{
        showUser(user){
            this.$store.commit('selectUser', user);
            this.$store.commit('pushMode', 'showUser');
        },
        addUser(){
            this.$store.commit('selectNewUser');
            this.$store.commit('pushMode', 'newUser');
        },
    },
    mounted(){
        this.$store.dispatch('getUsers');
    }
}
</script>


<style scoped>

.user-list-header{
    margin:15px 0 15px 0;
    font-size:22px;
    font-weight:600;
}

.user-list{
    list-style-type: none;
    padding:0;
    margin:0;
}

.user-management-container{
    padding:0 8px;
    height:100%;
    overflow:auto;
}

</style>