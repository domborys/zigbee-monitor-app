<template>
    <form class="password-form-container" @submit.prevent="changePassword">
        <h2 class="side-panel-h2 login-header">Zmiana hasła</h2>
        <div class="input-label-group">
            <label for="oldPasswordInput" class="text-label">Stare hasło</label>
            <input type="password" class="text-input" v-model="oldPassword" id="oldPasswordInput">
        </div>
        <div class="input-label-group">
            <label for="newPasswordInput" class="text-label">Nowe hasło</label>
            <input type="password" class="text-input" v-model="newPassword" id="newPasswordInput">
        </div>
        <div v-if="isError" class="error-message">
            {{ errorMsg }}
        </div>
        <div class="buttons-right">
            <button type="button" class="button" @click="backToPreviousMode">Anuluj</button>
            <button type="submit" class="button">Zmień hasło</button>
        </div>
        <div v-if="passwordChangeSuccessful">
            Hasło zostało zmienione.
        </div>
    </form>
</template>

<script>

/**
 * Component with a form used for changing the password of currently logged in user.
 */
export default {
    name:"PasswordChangeForm",
    data(){
        return{
            oldPassword:'',
            newPassword:'',
            isError:false,
            errorMsg:'',
            passwordChangeSuccessful:false,
        }
    },

    methods:{
        async changePassword(){
            const passwords = {oldPassword:this.oldPassword, newPassword:this.newPassword};
            try{
                await this.$store.dispatch('changePassword', passwords);
                this.passwordChangeSuccessful = true;
                setTimeout(this.logout, 2000);
            }
            catch(error){
                console.log(error);
                this.showError('Wystąpił błąd podczas zmiany hasła.');
            }
        },
        showError(message){
            this.errorMsg = message;
            this.isError = true;
        },
        backToPreviousMode(){
            this.$store.commit('previousMode');
        },
        async logout(){
            await this.$store.dispatch('logout');
            this.$store.commit('replaceMode', 'login');
        }
    },

    
}
</script>

<style scoped>

.password-form-container{
    flex:0 300px;
}

.login-header{
    margin-top:16px;
}
</style>