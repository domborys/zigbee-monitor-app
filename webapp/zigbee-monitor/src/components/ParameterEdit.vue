<template>
    <form class="parameter-edit-container" @submit.prevent="saveParameter">
        <div class="parameter-edit-main">
            <h2 class="side-panel-h2">{{headerText}}</h2>
            <div class="input-label-group">
                <label for="parameterNameInput" class="text-label">Nazwa parametru</label>
                <input type="text" v-model="parameterName" class="text-input" :class="{'text-input-invalid':parameterNameError !== null}"  id="parameterNameInput">
                <div v-if="parameterNameError !== null" class="input-error-message">{{ parameterNameError }}</div>
            </div>
            <div class="radio-set-container">
                <div class="radio-set-legend">Sposób odczytu parametru</div>
                <div class="radio-set-content">
                    <div class="radio-item-container">
                        <input type="radio" v-model="readMode" class="radio-input" value="listen" name="parameterReadMode" id="parameterReadModeListen" aria-describedby="modeListenDescription">
                        <label for="parameterReadModeListen">Oczekuj na komunikat</label>
                    </div>
                    <div class="radio-item-container">
                        <input type="radio" v-model="readMode" class="radio-input" value="send" name="parameterReadMode" id="parameterReadModeSend" aria-describedby="modeSendDescription">
                        <label for="parameterReadModeSend">Wyślij komunikat i oczekuj na odpowiedź</label>
                    </div>
                    <div class="radio-item-container">
                        <input type="radio" v-model="readMode" class="radio-input" value="at" name="parameterReadMode" id="parameterReadModeAt" aria-describedby="modeAtDescription">
                        <label for="parameterReadModeAt">Odczytaj parametr AT</label>
                    </div>
                </div>
                <div v-if="readModeError !== null" class="input-error-message">{{ readModeError }}</div>
            </div>
            <div class="option-description">
                <span v-if="readMode === 'listen'" id="modeListenDescription">
                    Aplikacja będzie oczekiwać na komunikaty przysłane z urządzenia o zadanym formacie.
                </span>
                <span v-if="readMode === 'send'" id="modeSendDescription">
                    Aplikacja będzie wysyłać co określony czas komunikat od urządzenia a następnie oczekiwał na odpowiedź o zadanym formacie.
                </span>
                <span v-if="readMode === 'at'" id="modeAtDescription">
                    Aplikacja będzie wysyłać komentę AT do urządzenia i wyświetlać jej wynik. 
                </span>
            </div>
            <div v-if="readMode === 'listen'">
                <div class="input-label-group">
                    <label for="messagePrefixInput" class="text-label">Początek oczekiwanego komunikatu</label>
                    <input type="text" v-model="messagePrefix" class="text-input" id="messagePrefixInput">
                </div>
            </div>
            <div v-if="readMode === 'send'">
                <div class="input-label-group">
                    <label for="messageToSendInput" class="text-label">Komunikat do wysłania w celu odczytu wiadomości</label>
                    <input type="text" v-model="messageToSend" class="text-input" id="messageToSendInput">
                </div>
                <div class="input-label-group">
                    <label for="messageRefreshPeriodInput" class="text-label">Czas odświeżania w sekundach</label>
                    <input type="text" v-model="refreshPeriod" class="text-input refresh-time-input" :class="{'text-input-invalid':refreshPeriodError !== null}" id="messageRefreshPeriodInput">
                    <div v-if="refreshPeriodError !== null" class="input-error-message">{{ refreshPeriodError }}</div>
                </div>
                <div class="input-label-group">
                    <label for="receivedMessagePrefixInput" class="text-label">Początek oczekiwanego komunikatu</label>
                    <input type="text" v-model="messagePrefix" class="text-input" id="receivedMessagePrefixInput">
                </div>
            </div>
            <div v-if="readMode === 'at'">
                <div class="input-label-group">
                    <label for="atCommandName" class="at-data-label">Nazwa komendy AT</label>
                    <input type="text" v-model="atCommand" class="text-input at-command-input" id="atCommandName" :class="{'text-input-invalid':atCommandNameError !== null}"  maxlength="2">
                    <div v-if="atCommandNameError !== null" class="input-error-message">{{ atCommandNameError }}</div>
                </div>
                <div>
                    <div class="radio-set-legend">Format danych komendy AT</div>
                    <div class="radio-set-content">
                        <div class="radio-item-container">
                            <input type="radio" class="radio-input" v-model="atCommandFormat" name="atDataMode" id="atDataModeNone" value="none">
                            <label for="atDataModeNone">Brak danych</label>
                        </div>
                        <div class="radio-item-container">
                            <input type="radio" class="radio-input" v-model="atCommandFormat" name="atDataMode" id="atDataModeText" value="text">
                            <label for="atDataModeText">Dane w formacie tekstowym</label>
                        </div>
                        <div class="radio-item-container">
                            <input type="radio" class="radio-input" v-model="atCommandFormat" name="atDataMode" id="atDataModeHex" value="hex">
                            <label for="atDataModeHex">Dane w formacie heksadecymalnym</label>
                        </div>
                    </div>
                </div>
                <div class="input-label-group">
                    <label for="atCommandData" class="at-data-label">Dane komendy AT</label>
                    <input type="text" v-model="atCommandData" :disabled="atCommandFormat === 'none'" class="text-input" id="atCommandData">
                </div>
                <div class="input-label-group">
                    <label for="atRefreshPeriodInput" class="text-label">Czas odświeżania w sekundach</label>
                    <input type="text" v-model="refreshPeriod" class="text-input refresh-time-input" :class="{'text-input-invalid':refreshPeriodError !== null}" id="atRefreshPeriodInput">
                    <div v-if="refreshPeriodError !== null" class="input-error-message">{{ refreshPeriodError }}</div>
                </div>
                <div>
                    <div class="radio-set-legend">Format wyniku komendy</div>
                    <div class="radio-set-content">
                        <div class="radio-item-container">
                            <input type="radio" class="radio-input" v-model="atCommandResultFormat" name="atCommandResponseFormat" id="atCommandResponseFormatText" value="text">
                            <label for="atCommandResponseFormatText">Dane tekstowe</label>
                        </div>
                        <div class="radio-item-container">
                            <input type="radio" class="radio-input" v-model="atCommandResultFormat" name="atCommandResponseFormat" id="atCommandResponseFormatDec" value="dec">
                            <label for="atCommandResponseFormatDec">Liczba dziesiętna</label>
                        </div>
                        <div class="radio-item-container">
                            <input type="radio" class="radio-input" v-model="atCommandResultFormat" name="atCommandResponseFormat" id="atCommandResponseFormatHex" value="hex">
                            <label for="atCommandResponseFormatHex">Dane w formacie heksadecymalnym</label>
                        </div>
                    </div>
                    <div v-if="resultFormatError !== null" class="input-error-message">{{ resultFormatError }}</div>
                </div>
            </div>
        </div>
        <div class="parameter-edit-footer">
            <div class="parameter-edit-footer-buttons">
                <button type="button" class="button footer-button" @click="discardChanges">Anuluj</button>
                <button type="submit" class="button footer-button">{{submitButtonText}}</button>
            </div>
            <div>
                <div v-if="formSubmitAttempted && !isFormValid" class="input-error-message">{{ generalError }}</div>
            </div>
        </div>
    </form>
</template>

<script>

import utils from '../utils';

export default {
    name:"ParameterEdit",
    components:{
        
    },
    props:{
        
    },
    data(){
        return{
            atCommandFormat:'none',
            rawMessagePrefix:'',
            rawMessageToSend:'',
            rawCommandData:'',
            parameterNameError:null,
            readModeError:null,
            refreshPeriodError: null,
            atCommandNameError: null,
            resultFormatError: null,
            generalError:null,
            formSubmitAttempted:false,
        }
    },
    computed:{
        readingConfig(){
            return this.$store.state.editedReadingConfig;
        },
        parameterName:{
            get(){
                return this.readingConfig.name;
            },
            set(value){
                this.validateParameterName(value);
                this.$store.commit('setEditedReadingConfigParam', {name:'name', value:value});
            }
        },
        readMode:{
            get(){
                return this.readingConfig.mode;
            },
            set(value){
                this.validateReadMode(value);
                this.$store.commit('setEditedReadingConfigParam', {name:'mode', value:value});
            }
        },
        
        messagePrefix:{
            get(){
                return this.readingConfig.messagePrefix === null ? '' : atob(this.readingConfig.messagePrefix);
            },
            set(value){
                //this.rawMessagePrefix = value;
                this.$store.commit('setEditedReadingConfigParam', {name:'messagePrefix', value:btoa(value)});
            }
        },
        messageToSend:{
            get(){
                return this.readingConfig.messageToSend === null ? '' : atob(this.readingConfig.messageToSend);
            },
            set(value){
                //this.rawMessageToSend = value;
                this.$store.commit('setEditedReadingConfigParam', {name:'messageToSend', value:btoa(value)});
            }
        },
        refreshPeriod:{
            get(){
                return this.readingConfig.refreshPeriod;
            },
            set(value){
                this.validateRefreshPeriod(value);
                this.$store.commit('setEditedReadingConfigParam', {name:'refreshPeriod', value:value});
            }
        },
        atCommand:{
            get(){
                return this.readingConfig.atCommand;
            },
            set(value){
                this.validateAtCommandName(value);
                this.$store.commit('setEditedReadingConfigParam', {name:'atCommand', value:value});
            }
        },
        atCommandData:{
            get(){
                if(this.atCommandFormat === 'text'){
                    return utils.decodeMessageToText(this.readingConfig.atCommandData);
                }
                else if(this.atCommandFormat === 'hex'){
                    return utils.decodeMessageToHex(this.readingConfig.atCommandData);
                }
                else{
                    return null;
                }
            },
            set(value){
                //this.rawCommandData = value;
                let commandBase64 = this.getEncodedCommandData(value);
                this.$store.commit('setEditedReadingConfigParam', {name:'atCommandData', value:commandBase64});
            }
        },
        atCommandResultFormat:{
            get(){
                return this.readingConfig.atCommandResultFormat;
            },
            set(value){
                this.validateResultFormat(value);
                this.$store.commit('setEditedReadingConfigParam', {name:'atCommandResultFormat', value:value});
            }
        },
        newConfigMode(){
            return this.$store.getters.mode === 'newReadingConfig';
        },
        headerText(){
            return this.newConfigMode ? 'Nowy parametr' : 'Edycja parametru';
        },
        submitButtonText(){
            return this.newConfigMode ? 'Dodaj' : 'Zapisz';
        },
        isFormValid(){
            const common = this.parameterNameError === null && this.readModeError === null;
            let modeSpecific = true;
            if(this.readMode === 'listen'){
                modeSpecific = true;
            }
            else if(this.readMode === 'send'){
                modeSpecific = this.refreshPeriodError === null;
            }
            else if(this.readMode === 'at'){
                modeSpecific = this.refreshPeriodError === null && this.atCommandNameError === null && this.resultFormatError === null;
            }
            return common && modeSpecific;
        }

        
    },
    methods:{
        discardChanges(){
            this.$store.commit('discardEditedReadingConfig');
            this.$store.commit('previousMode');
        },
        saveParameter(){
            if(this.checkIfValid()){
                this.$store.commit('saveEditedReadingConfig');
                this.$store.commit('previousMode');
            }
        },
        getEncodedCommandData(commandData){
            if(this.atCommandFormat === 'text'){
                return utils.encodeTextMessage(commandData);
            }
            else if(this.atCommandFormat === 'hex'){
                return utils.encodeHexMessage(commandData);
            }
            else
                return null;
        },
        validateParameterName(parameterName){
            if(typeof parameterName === 'undefined')
                parameterName = this.parameterName;
            if(typeof parameterName === 'string' && parameterName.trim().length > 0){
                this.parameterNameError = null;
                return true;
            }
            else{
                this.parameterNameError = 'Nazwa parametru nie może być pusta.';
                return false;
            }  
        },
        validateReadMode(readMode){
            if(typeof readMode === 'undefined')
                readMode = this.readMode;
            if(readMode !== null){
                this.readModeError = null;
                return true;
            }
            else{
                this.readModeError = 'Proszę wybrać sposób odczytu parametru';
                return false;
            }  
        },
        validateRefreshPeriod(refreshPeriod){
            if(typeof refreshPeriod === 'undefined')
                refreshPeriod = this.refreshPeriod;
            if(utils.isNumeric(refreshPeriod)){
                this.refreshPeriodError = null;
                return true;
            }
            else{
                this.refreshPeriodError = 'Czas odświeżania powinien być liczbą.';
                return false;
            }
        },
        validateAtCommandName(name){
            if(typeof name === 'undefined')
                name = this.atCommand;
            if(typeof name === 'string' && name.length === 2){
                this.atCommandNameError = null;
                return true;
            }
            else{
                this.atCommandNameError = 'Nazwa komendy AT powinna składać się z dwóch znaków';
                return false;
            }
        },
        validateResultFormat(resultFormat){
            if(typeof resultFormat === 'undefined')
                resultFormat = this.atCommandResultFormat;
            if(resultFormat !== null){
                this.resultFormatError = null;
                return true;
            }
            else{
                this.resultFormatError = 'Proszę wybrać format wyniku.';
                return false;
            }
        },
        checkIfValid(){
            this.formSubmitAttempted = true;
            this.validateParameterName();
            this.validateReadMode();
            this.validateRefreshPeriod();
            this.validateAtCommandName();
            this.validateResultFormat();
            const isValid = this.isFormValid;
            if(isValid){
                this.generalError = null;
            }
            else{
                this.generalError = 'Proszę poprawić błędy.';
            }
            return isValid;
        },
        setAtCommandData(newCommandData){
            this.$store.commit('setEditedReadingConfigParam', {name:'atCommandData', value:newCommandData});
        }
    },
    watch:{
        /*
        messagePrefix(newValue){

        }*/
        /*
        messagePrefix(newMessage){
            this.$store.commit('setEditedReadingConfigParam', {name:'messagePrefix', value:btoa(newMessage)});
        },
        messageToSend(newMessage){
            this.$store.commit('setEditedReadingConfigParam', {name:'messageToSend', value:btoa(newMessage)});
        }*/
        /*
        atCommandFormat(newFormat, oldFormat){
            if(newFormat === 'none'){
                this.setAtCommandData(null);
            }
            else if(newFormat === 'text'){
                this.setAtCommandData(null);
            }
        }*/
    },
    mounted(){
        if(this.readingConfig.atCommandData === null)
            this.atCommandFormat = 'none';
        else
            this.atCommandFormat = 'hex';
    }
    
}
</script>


<style scoped>

.parameter-edit-container{
    height:100%;
    display: flex;
    flex-direction: column;
}

.parameter-edit-main{
    flex:auto;
    overflow:auto;
    min-height:0;
    border-bottom:1px solid #E6E6FA;
}

.parameter-edit-footer{
    flex:none;
    box-sizing:border-box;
    padding-top:8px;
}

.parameter-edit-footer-buttons{
    display:flex;
}

.footer-button{
    flex:1;
}

.at-command-input, .input-label-group .at-command-input{
    width:50px;
}

.refresh-time-input, .input-label-group .refresh-time-input{
    width:60px;
}

</style>