import api from '../api';
export default {
    state: () => ({
        users:[],
        selectedUser:null,
    }),
    getters: {},
    mutations: {
        setUsers(state, users){
            state.users = users;
        },
        addUser(state, user){
            state.users.push(user);
        },
        modifyUser(state, user){
            const index = state.users.findIndex(u => u.id === user.id);
            state.users.splice(index, 1, user);
        },
        deleteUser(state, user){
            const index = state.users.findIndex(u => u.id === user.id);
            state.users.splice(index, 1);
        },
        selectUser(state, user){
            state.selectedUser = user;
        },
        selectNewUser(state){
            state.selectedUser = {id:null, username:null, password:null, role:'user', disabled:false};
        }
    },
    actions: {
        async getUsers(context){
            const users = await api.getUsers();
            context.commit('setUsers', users);
        },
        async addUser(context, user){
            const returnedUser = await api.addUser(user);
            context.commit('addUser', returnedUser);
        },
        async modifyUser(context, user){
            const returnedUser = await api.modifyUser(user);
            context.commit('modifyUser', returnedUser);
        },
        async deleteUser(context, user){
            await api.deleteUser(user);
            context.commit('deleteUser', user);
        }
    },
    
};