<template>
    <form class="login-form-container" @submit.prevent="login">
        <h2 class="side-panel-h2 login-header">Logowanie</h2>
        <div class="input-label-group">
            <label for="usernameInput" class="text-label">Użytkownik</label>
            <input type="text" class="text-input" v-model="username" id="usernameInput">
        </div>
        <div class="input-label-group">
            <label for="passwordInput" class="text-label">Hasło</label>
            <input type="password" class="text-input" v-model="password" id="passwordInput">
        </div>
        <div v-if="isError" class="error-message">
            {{ errorMsg }}
        </div>
        <div class="buttons-right">
            <button type="submit" class="button">Zaloguj</button>
        </div>
    </form>
</template>

<script>


export default {
    name:"LoginForm",
    components:{
        
    },
    props:{
        
    },
    data(){
        return{
            username:'',
            password:'',
            isError:false,
            errorMsg:''
        }
    },

    methods:{
        async login(){
            const credentials = {username:this.username, password:this.password};
            try{
                await this.$store.dispatch('login', credentials);
                this.$store.commit('replaceMode', 'view');
                this.$store.dispatch('downloadLayers')
                    .then(() => this.$store.dispatch('downloadDiscoveryResults'))
            }
            catch(error){
                console.log(error);
                this.showError('Nieprawidłowa nazwa użytkownika lub hasło.');
            }
        },
        showError(message){
            this.errorMsg = message;
            this.isError = true;
        }
    },

    
}
</script>

<style scoped>

.login-form-container{
    flex:0 300px;
}

.login-header{
    margin-top:16px;
}
</style>