<template>
  <div class="login-container-parent"></div>
  <div class="half_width_and_center" style="top: 10%">
    <ui5-card style="justify-content: center">
      <div style="width: 50%; margin: 0 auto; justify-content: center; text-align: center">
        <h3 style="color: #00455d;">Система подачи заявок ИОХК</h3>
        <ui5-button icon="visits" @click="e => showPopover(e, 'Вход в систему')">Вход в систему</ui5-button><br/><br/>
        <ui5-button icon="add-employee" @click="e => {
          if (states.length === 0) {getStates()}
          showPopover(e, 'Регистрация')
        }">Регистрация</ui5-button><br/><br/>
        <ui5-button icon="private" @click="e => showPopover(e, 'Восстановление пароля')">Восстановление пароля</ui5-button><br/><br/>
      </div>
    </ui5-card>
  </div>
  <form ref="login_form"  @submit="formAction">
    <ui5-dialog ref="dialog" style="z-index: 16" resizable draggable>
        <ui5-bar slot="header">
          <ui5-title level="H5" slot="startContent">{{dialogTitle}}</ui5-title>
          <ui5-button design="Emphasized" slot="endContent" icon="decline" @click="e => this.$refs.dialog.close(e.current)"></ui5-button>
        </ui5-bar>
      <div v-if="dialogTitle === 'Вход в систему'">
          <table>
            <tr>
              <td style="text-align: right">
                <ui5-label required show-colon>Вход по</ui5-label>
              </td>
              <td>
                <ui5-radio-button name="AuthType"
                                  text="Телефон"
                                  @change="changeAuthType('phone')" checked>
                </ui5-radio-button><br/>
                <ui5-radio-button name="AuthType"
                                  text="Почта"
                                  @change="changeAuthType('email')">
                </ui5-radio-button>
              </td>
            </tr>
            <tr>
              <td style="text-align: right">
                <ui5-label for="login_username" required show-colon>Логин</ui5-label>
              </td>
              <td>
                <ui5-input v-if="!(phoneLogin)" type="Email" id="login_username" ref="login_username" required />
                <PhoneField v-if="phoneLogin" ref="login_phone"
                            v-bind:phoneValueState="loginPhoneValueState"
                            v-bind:phoneStateText="loginPhoneStateText" />
              </td>
            </tr>
            <tr>
              <td style="text-align: right">
                <ui5-label for="login_password" required show-colon>Пароль</ui5-label>
              </td>
              <td>
                <PasswordField id="login_password" ref="login_password" />
              </td>
            </tr>
          </table>
      </div>
      <div v-if="dialogTitle === 'Регистрация'">
        <table style="border: 0; width: 50vw;">
          <tr>
            <td style="text-align: right">
              <ui5-label for="reg_state" required show-colon>Государство</ui5-label>
            </td>
            <td>
              <ui5-select id="reg_state" ref="reg_state">
                <ui5-option v-for="state in states"
                            :value="state.id"
                            :selected="state.name === 'Россия'">
                  {{state.name}}
                </ui5-option>
              </ui5-select>
            </td>
          </tr>
          <tr>
            <td style="text-align: right">
              <ui5-label for="reg_surname" required show-colon>Фамилия</ui5-label>
            </td>
            <td>
              <ui5-input type="Text" id="reg_surname" ref="reg_surname" required />
            </td>
          </tr>
          <tr>
            <td style="text-align: right">
              <ui5-label for="reg_name" required show-colon>Имя</ui5-label>
            </td>
            <td>
              <ui5-input type="Text" id="reg_name" ref="reg_name" required />
            </td>
          </tr>
          <tr>
            <td style="text-align: right">
              <ui5-label for="reg_patronymic" show-colon>Отчество</ui5-label>
            </td>
            <td>
              <ui5-input type="Text" id="reg_patronymic" ref="reg_patronymic" />
            </td>
          </tr>
          <tr>
            <td style="text-align: right">
              <ui5-label for="reg_sex" required show-colon>Пол</ui5-label>
            </td>
            <td>
              <ui5-switch id="reg_sex" ref="reg_sex" text-on="М" text-off="Ж" />
            </td>
          </tr>
          <tr>
            <td style="text-align: right">
              <ui5-label for="reg_birthday" required show-colon>Дата рождения</ui5-label>
            </td>
            <td>
              <ui5-date-picker id="reg_birthday"
                               ref="reg_birthday"
                               format-pattern="dd.MM.yyyy"
                               required/>
            </td>
          </tr>
          <tr>
            <td style="text-align: right">
              <ui5-label for="reg_email" required show-colon>Email</ui5-label>
            </td>
            <td>
              <ui5-input type="Email" id="reg_email" ref="reg_email"
                         :value-state="regEmailValueState"
                         @change="e => checkEmailUnique()" required>
                <div slot="valueStateMessage">{{ regEmailStateText }}</div>
              </ui5-input>
            </td>
          </tr>
          <tr>
            <td style="text-align: right">
              <ui5-label for="reg_phone" required show-colon>Телефон</ui5-label>
            </td>
            <td>
              <PhoneField ref="reg_phone"
                          v-bind:phoneValueState="regPhoneValueState"
                          v-bind:phoneStateText="regPhoneStateText"
                          v-bind:changePhoneAction="checkPhoneUnique" />
            </td>
          </tr>
          <tr>
            <td style="text-align: right">
              <ui5-label for="reg_role" required show-colon>Роль пользователя</ui5-label>
            </td>
            <td>
              <ui5-select id="reg_role" ref="reg_role" @change="this.selectedRole = this.$refs.reg_role.selectedOption.innerText">
                <ui5-option selected>Преподаватели</ui5-option>
                <ui5-option>Участники</ui5-option>
              </ui5-select>
            </td>
          </tr>
          <tr v-if="this.selectedRole === 'Преподаватели'">
            <td style="text-align: right">
              <ui5-label for="reg_oo_fullname" required show-colon>Полное наименование ОО</ui5-label>
            </td>
            <td>
              <ui5-textarea id="reg_oo_fullname" ref="reg_oo_fullname" rows="10" required></ui5-textarea>
            </td>
          </tr>
          <tr v-if="this.selectedRole === 'Преподаватели'">
            <td style="text-align: right">
              <ui5-label for="reg_oo_shortname" required show-colon>Краткое наименование ОО</ui5-label>
            </td>
            <td>
              <ui5-textarea id="reg_oo_shortname" ref="reg_oo_shortname" rows="10" required></ui5-textarea>
            </td>
          </tr>
          <tr>
            <td style="text-align: right">
              <ui5-label for="reg_password_1" required show-colon>Пароль</ui5-label>
            </td>
            <td>
              <PasswordField id="reg_password_1" ref="reg_password_1" />
            </td>
          </tr>
          <tr>
            <td style="text-align: right">
              <ui5-label for="reg_password_2" required show-colon>Подтверждение пароля</ui5-label>
            </td>
            <td>
              <PasswordField id="reg_password_2" ref="reg_password_2" />
            </td>
          </tr>
          <tr>
            <td style="text-align: right">
              <ui5-label for="reg_personal" required show-colon>
                Согласие на обработку <br/>персональных данных
              </ui5-label><br/>
              <ui5-button icon="document-text" @click="e => this.$refs.personal_popover.showAt(e.target)"></ui5-button>
              <ui5-popover ref="personal_popover" placement-type="Top" header-text="Согласие на обработку ПДн">
                <p style="text-align: justify; font-size: 16px">В соответствии с требованиями статьи 9 Федерального закона от 27 июля 2006 г. № 152-ФЗ «О персональных данных»,
                свободно, по своей волей и в своем интересе даю согласие Иркутскому областному художественному колледжу им. И.Л. Копылова
                на обработку (любое действие (операцию) или совокупность действий (операций), совершаемых с использованием средств автоматизации
                или без использования таких средств с персональными данными, включая сбор, запись, систематизацию, накопление,
                хранение, уточнение (обновление, изменение), извлечение, использование, передачу (распространение, предоставление,
                доступ), обезличивание, блокирование, удаление, уничтожение) следующих персональных данных:<br/>
                фамилия, имя, отчество (последнее - при наличии);<br/>
                дата рождения;<br/>
                адрес электронной почты;<br/>
                номер контактного телефона.<br/>
                Настоящее согласие действует на период до истечения сроков хранения соответствующей информации или
                документов, содержащих указанную информацию, определяемых в соответствии с законодательством Российской Федерации.<br/>
                Отзыв согласия осуществляется в соответствии с законодательством Российской Федерации.
                </p>
                <div slot="footer" style="display: flex; justify-content: flex-end; width: 100%;
                                          align-items: center; padding: 0.5rem 0;">
                  <ui5-button design="Emphasized" @click="e => this.$refs.personal_popover.close()">OK</ui5-button>
                </div>
              </ui5-popover>
            </td>
            <td>
              <ui5-switch id="reg_personal" ref="reg_personal"
                          text-on="Да" text-off="Нет"
                          @change="e => this.personalAgree = e.target._state.checked"/>
            </td>
          </tr>
        </table>
      </div>
      <div v-if="dialogTitle === 'Восстановление пароля'">
        <table>
          <tr>
            <td style="text-align: right">
              <ui5-label for="repair_email" required show-colon>Email, указанный при регистрации</ui5-label>
            </td>
            <td>
              <ui5-input type="Email" id="repair_email" ref="repair_email" required />
            </td>
          </tr>
        </table>
      </div>
      <div slot="footer" style="display: flex; justify-content: flex-end; width: 100%; align-items: center">
        <div v-if="profileChangeError.length > 0" >
          <ui5-message-strip design="Negative" hide-close-button>
            {{profileChangeError}}
          </ui5-message-strip>
        </div>&nbsp;
        <ui5-button v-if="dialogTitle === 'Вход в систему'" design="Emphasized" submits>Войти</ui5-button>
        <ui5-button v-if="dialogTitle === 'Регистрация'"
                    design="Emphasized"
                    submits :disabled="!(personalAgree)">Зарегистрироваться</ui5-button>
        <ui5-button v-if="dialogTitle === 'Восстановление пароля'" design="Emphasized" submits>Восстановить</ui5-button>
      </div>
    </ui5-dialog>
  </form>
  <PreLoader ref="preLoader" />
</template>

<script>
import PreLoader from '../App.vue'
import PasswordField from '../components/PasswordField.vue'
import PhoneField from "../components/PhoneField.vue";
import {apiRequest} from "../additional/functions/api_request.js";

export default {
  name: 'Login',
  components: {
    PhoneField,
    PreLoader,
    PasswordField
  },
  data() {
    return {
      profileChangeError: '',
      phoneLogin: true,
      regPhoneField: '',
      loginPhoneField: '',
      regPhoneValueState: 'None',
      regPhoneStateText: '',
      loginPhoneValueState: 'None',
      loginPhoneStateText: '',
      regEmailValueState: 'None',
      regEmailStateText: '',
      dialogTitle: '',
      selectedRole: 'Преподаватели',
      personalAgree: false,
      states: []
    }
  },
  methods: {
    showPopover: function(e, header) {
      this.dialogTitle = header
      this.$refs.dialog.show(e.current)
      setTimeout(removeTableHeaderRow, 25)
    },
    async getStates() {
      apiRequest(
          this.$store.state.backendUrl+'/api/v1/auth/states/',
          'GET',
          false,
          null,
          false,
          false
      )
          .then(data => {
            this.states = data.states
          })
    },
    async formAction(e) {
      e.preventDefault()
      let preloader = this.$refs.preLoader
      if (this.dialogTitle === 'Регистрация') {
        if ((this.checkPasswords() === false) ||
            (this.regEmailValueState === 'Error') ||
            (this.regPhoneValueState === 'Error') ||
            (this.$refs.reg_password_1.valueState !== 'None') ||
            (this.$refs.reg_password_2.valueState !== 'None')) {
          return false
        }
        this.$refs.dialog.close()
        preloader.usePreloader()
        let data = {
          'state': this.$refs.reg_state.selectedOption.value,
          'surname': this.$refs.reg_surname.value,
          'name': this.$refs.reg_name.value,
          'patronymic': this.$refs.reg_patronymic.value,
          'sex': this.$refs.reg_sex._state.checked,
          'birthday': this.$refs.reg_birthday.value,
          'phone': this.$refs.reg_phone.componentPhoneField,
          'email': this.$refs.reg_email.value,
          'role': this.$refs.reg_role.selectedOption.innerText,
          'oo_fullname': '',
          'oo_shortname': '',
          'password': this.$refs.reg_password_1.passwordStr,
        }
        if (data.role === 'Преподаватели') {
          data.oo_fullname = this.$refs.reg_oo_fullname.value
          data.oo_shortname = this.$refs.reg_oo_shortname.value
        }
        apiRequest(
            this.$store.state.backendUrl + '/api/v1/auth/registration/',
            'POST',
            false,
            data,
            false,
            false
        )
            .then(data => {
              if (data.error) {
                this.profileChangeError = data.error
                this.$refs.dialog.show()
              } else {
                showMessage('success', data.success, false)
              }
              preloader.usePreloader()
            })
      }
      else if (this.dialogTitle === 'Вход в систему') {
        preloader.usePreloader()
        this.$refs.dialog.close()
        let username = ''
        let password = this.$refs.login_password.passwordStr
        if (this.phoneLogin) {
          username = this.$refs.login_phone.componentPhoneField
        } else {
          username = this.$refs.login_username.value
        }
        this.$store.dispatch('AUTH_REQUEST', { username, password}).then(() => {
          if (getUrlParameter('nextUrl')) {
            this.$router.push({ path: getUrlParameter('nextUrl') })
          } else {
            this.$router.push('/main')
          }
        })
            .catch((error) => {
              this.profileChangeError = error
              this.$refs.dialog.show()
              preloader.usePreloader()
            })
      } else {

      }
    },
    changeAuthType(type) {
      this.phoneLogin = type === 'phone';
    },
    async checkPhoneUnique() {
      if (this.$refs.reg_phone.componentPhoneField.length !== 18) {
        this.regPhoneValueState = 'Error'
        this.regPhoneStateText = 'Некорректный номер телефона'
        return false
      }
      apiRequest(
          this.$store.state.backendUrl+'/api/v1/auth/check_phone/',
          'POST',
          false,
          {
            'phone': this.$refs.reg_phone.componentPhoneField
          },
          false,
          true
      )
          .then(resp => {
            if (resp.status === 200) {
              this.regPhoneValueState = 'Success'
              this.regPhoneStateText = 'Указанный номер телефона еще не зарегистрирован'
            } else {
              this.regPhoneValueState = 'Error'
              this.regPhoneStateText = 'Номер ' + this.regPhoneField+' уже зарегистрирован'
            }
          })
    },
    async checkEmailUnique() {
      apiRequest(
          this.$store.state.backendUrl+'/api/v1/auth/check_email/',
          'POST',
          false,
          {
            'email': this.$refs.reg_email.value
          },
          false,
          true
      )
          .then(resp => {
            if (resp.status === 200) {
              this.regEmailValueState = 'Success'
              this.regEmailStateText = 'Указанный email еще не зарегистрирован'
            } else {
              this.regEmailValueState = 'Error'
              this.regEmailStateText = 'Email уже зарегистрирован'
            }
          })
    },
    checkPasswords() {
      if ((this.$refs.reg_password_1.passwordStr.length > 0) && (this.$refs.reg_password_2.passwordStr.length > 0)) {
        if (this.$refs.reg_password_1.passwordStr.length < 8) {
          this.$refs.reg_password_1.valueState = 'Error'
          this.$refs.reg_password_1.valueStateText = 'Минимальная длина пароля - 8 символов'
          return false
        }
        if (this.$refs.reg_password_1.passwordStr !== this.$refs.reg_password_2.passwordStr) {
          this.$refs.reg_password_1.valueState = 'Error'
          this.$refs.reg_password_2.valueState = 'Error'
          this.$refs.reg_password_1.valueStateText = 'Введенные пароли не совпадают'
          this.$refs.reg_password_2.valueStateText = 'Введенные пароли не совпадают'
          return false
        } else {
          this.$refs.reg_password_1.valueState = 'None'
          this.$refs.reg_password_2.valueState = 'None'
        }
      }
      return true
    }
  },
  watch: {
    LoginPhoneField() {
      this.checkPhoneLength('login');
    },
  }
}

</script>

<style>

.login-container-parent {
  background-image: url('/media/imgs/login-back.jpg');
  background-size: cover;
  pointer-events: none;
  position: absolute;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  -webkit-filter: blur(5px);
}
.half_width_and_center{
  position: relative;
  z-index: 5;
  width: 50vw;
  margin: 0 auto;
}

</style>