<template>
    <form @submit.prevent="saveUser" class="one-column-container user-edit-container">
        <div class="heading-back-group">
            <button type="button" class="heading-back-button" @click="back"></button>
            <h2 class="heading-back-heading">{{ headerText }}</h2>
        </div>
        <div class="user-edit-main">
            <div class="input-label-group">
                <label for="userNameInput" class="text-label">Nazwa użytkownika</label>
                <input type="text" class="text-input" v-model="username" id="userNameInput">
                <div v-if="usernameError !== null" class="input-error-message">{{ usernameError }}</div>
            </div>
            <div v-if="!newUserMode" class="radio-set-container">
                <div class="radio-item-container">
                    <input type="checkbox" v-model="isPasswordChanged" class="checkbox-input" id="checkboxChangePassword">
                    <label for="checkboxChangePassword">Zmień hasło</label>    
                </div>
            </div>
            <div class="input-label-group">
                <label for="passwordInput" class="text-label">Hasło</label>
                <input type="password" class="text-input" v-model="password" id="passwordInput" :disabled="passwordFieldDisabled">
                <div v-if="passwordError !== null" class="input-error-message">{{ passwordError }}</div>
            </div>
            <div class="radio-set-container">
                <div class="radio-set-legend">Rola</div>
                <div class="radio-set-content">
                    <div class="radio-item-container">
                        <input type="radio" v-model="role" class="radio-input" value="user" name="userRole" id="userRoleUser" aria-describedby="roleUserDescription">
                        <label for="userRoleUser">Użytkownik</label>
                    </div>
                    <div class="radio-item-container">
                        <input type="radio" v-model="role" class="radio-input" value="admin" name="userRole" id="userRoleAdmin" aria-describedby="roleAdminDescription">
                        <label for="userRoleAdmin">Administrator</label>
                    </div>
                </div>
            </div>
            <div class="option-description">
                <span v-if="role === 'user'" id="roleUserDescription">
                    Użytkownik może odczytywać stan urządzeń, dodawać, modyfikować i usuwać mapy i urządzenia, a także wysyłać i odbierać pakiety od urządzeń.
                </span>
                <span v-if="role === 'admin'" id="roleAdminDescription">
                    Administrator ma wszystkie uprawnienia zwykłego użytwkownika i dodatkowo może zarządzać kontami użytkowników.
                </span>
            </div>
            <div class="radio-set-container">
                <div class="radio-item-container">
                    <input type="checkbox" v-model="userDisabled" class="checkbox-input" id="checkboxUserDisabled">
                    <label for="checkboxUserDisabled">Zablokuj użytkownika</label>
                </div>
            </div>
        </div>
        <div class="layer-edit-footer">
            <div class="buttons-container">
                <button type="button" @click="back" class="button flex-button">Anuluj</button>
                <button type="submit" class="button flex-button">{{ submitButtonText }}</button>
            </div>
            <div v-if="formSubmitAttempted && !isFormValid" class="input-error-message">{{ generalError }}</div>
        </div>
    </form> 
</template>

<script>

export default {
    name:"UserEdit",
    data(){
        return{
            isPasswordChanged:false,
            usernameError: null,
            passwordError: null,
            generalError:null,
            formSubmitAttempted:false,
        }
    },
    components:{
        
    },
    props:{
    },
    computed:{
        user(){
            return this.$store.state.users.selectedUser;
        },
        mode(){
            return this.$store.getters.mode;
        },
        newUserMode(){
            return this.mode === 'newUser';
        },
        headerText(){
            return this.newUserMode ? 'Dodawanie użytkownika' : 'Edycja użytkownika ' + this.user.username;
        },
        passwordFieldDisabled(){
            return !this.newUserMode && !this.isPasswordChanged;
        },
        submitButtonText(){
            return this.newNodeMode ? 'Dodaj' : 'Zapisz';
        },
        isFormValid(){
            return this.usernameError === null && this.passwordError === null;
        },
        username:{
            get(){
                return this.user.username;
            },
            set(value){
                this.validateUsername(value);
                this.$store.commit('setSelectedUserParam', {name:'username', value:value});
            }
        },
        password:{
            get(){
                return this.user.password;
            },
            set(value){
                this.validatePassword(value);
                this.$store.commit('setSelectedUserParam', {name:'password', value:value});
            }
        },
        role:{
            get(){
                return this.user.role;
            },
            set(value){
                this.$store.commit('setSelectedUserParam', {name:'role', value:value});
            }
        },
        userDisabled:{
            get(){
                return this.user.disabled;
            },
            set(value){
                this.$store.commit('setSelectedUserParam', {name:'disabled', value:value});
            }
        }
    },
    methods:{
        validateUsername(username){
            if(typeof username === 'undefined')
                username = this.username;
            if(typeof username === 'string' && username.trim().length > 0){
                this.usernameError = null;
                return true;
            }
            else{
                this.usernameError = 'Nazwa użytkownika nie może być pusta.';
                return false;
            }
        },
        validatePassword(password){
            if(typeof password === 'undefined')
                password = this.password;
            if(this.passwordFieldDisabled){
                this.passwordError = null;
                return true;
            }
            if(typeof password === 'string' && password.trim().length > 0){
                this.passwordError = null;
                return true;
            }
            else{
                this.passwordError = 'Hasło nie może być puste.';
                return false;
            }
        },
        checkIfValid(){
            this.formSubmitAttempted = true;
            this.validateUsername();
            this.validatePassword();
            const isValid = this.isFormValid;
            if(isValid){
                this.generalError = null;
            }
            else{
                this.generalError = 'Proszę poprawić błędy.';
            }
            return isValid;
        },
        back(){
            this.$store.commit('reselectUser');
            this.$store.commit('previousMode');
        },
        async saveUser(){
            if(!this.checkIfValid()){
                return;
            }
            if(this.passwordFieldDisabled){
                this.password = null;
            }
            if(this.newUserMode){
                await this.$store.dispatch('addUser', this.user);
            }
            else{
                await this.$store.dispatch('modifyUser', this.user);
            }
            this.back();
        }
    },
    watch:{
        isPasswordChanged(newState){
            if(newState === false){
                this.password = null;
            }
        }
    }
}
</script>


<style scoped>

.user-edit-main{
    padding:0 8px 15px 8px;
    flex:auto;
    overflow:auto;
    min-height:0;
    border-bottom:1px solid #E6E6FA;
}

.buttons-container{
    text-align:right;
    display:flex;
}

.user-edit-container{
    height:100%;
    display: flex;
    flex-direction: column;
}

.flex-button{
    flex:1;
    margin:2px;
}

.layer-edit-footer{
    padding:3px;
}

</style>