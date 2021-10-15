<template>
    <div>
        <div class="heading-back-group">
            <button type="button" class="heading-back-button" @click="back"></button>
            <h2 class="heading-back-heading">{{ headerText }}</h2>
        </div>
        <form @submit.prevent="saveUser">
            <div class="input-label-group">
                <label for="userNameInput" class="text-label">Nazwa użytkownika</label>
                <input type="text" class="text-input" v-model="username" id="userNameInput">
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
            <div>
                <button type="submit" class="button">{{ submitButtonText }}</button>
            </div>
        </form>
    </div> 
</template>

<script>

export default {
    name:"UserEdit",
    data(){
        return{
            isPasswordChanged:false,
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
        username:{
            get(){
                return this.user.username;
            },
            set(value){
                this.$store.commit('setSelectedUserParam', {name:'username', value:value});
            }
        },
        password:{
            get(){
                return this.user.password;
            },
            set(value){
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
        back(){
            this.$store.commit('reselectUser');
            this.$store.commit('previousMode');
        },
        async saveUser(){
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


</style>