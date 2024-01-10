<template>
  <LkBase ref="baseComponent">
    <slot>
      <ui5-card class="full-card">
        <ui5-card-header slot="header"
                         title-text="Пользователи">
        </ui5-card-header>
        <div style="height:  80vh">
          <PaginationTable v-if="this.fieldsArray.length > 0"
                           ref="pagination_table"
                           v-bind:tableMode="tableMode"
                           v-bind:recsURL="recsURL"
                           v-bind:recAddURL="recAddURL"
                           v-bind:recEditURL="recEditURL"
                           v-bind:recDeleteURL="recDeleteURL"
                           v-bind:searchRow="searchRow"
                           v-bind:changeShowFields="changeShowFields"
                           v-bind:colCount="colCount"
                           v-bind:activeRow="activeRow"
                           v-bind:activeRowEvent="showUserProfile"
                           v-bind:addButton="addButton"
                           v-bind:tableColumns="tableColumns"
                           v-bind:fieldsArray="fieldsArray"
                           v-bind:dataTableHeight="dataTableHeight"
          />
        </div>
      </ui5-card>
    </slot>
  </LkBase>
  <ui5-dialog ref="profileDialog">
    <div style="height: 99%">
      <ProfileForm ref="profile_form"
                   v-bind:isAdmin="true"
                   v-bind:profileData="selectedProfile"
                   v-bind:profileFormAction="checkUniqueData"
                   v-bind:passwordFormAction="changePassword" />
    </div>
    <div slot="footer" style="display: flex; justify-content: flex-end; width: 100%; align-items: center">
      <div style="flex: 1;"></div>
      <div v-if="profileChangeError.length > 0" >
        <ui5-message-strip design="Negative" hide-close-button>
          {{profileChangeError}}
        </ui5-message-strip>
      </div>&nbsp;
      <ui5-button design="Emphasized"
                  @click="$refs.profileDialog.close(); this.profileChangeError = ''">Закрыть</ui5-button>
    </div>
  </ui5-dialog>
</template>

<script>
import PaginationTable from "../../components/tables/PaginationTable.vue";
import LkBase from "../../components/LkBase.vue";
import ProfileForm from "../../components/ProfileForm.vue";
import {apiRequest} from "../../additional/functions/api_request.js";

export default {
  name: 'Users',
  components: {ProfileForm, LkBase, PaginationTable},
  data() {
    return {
      dataTableHeight: 68,
      states: [
        {
          id: 0,
          name: ''
        },
        {
          id: 1,
          name: 'Дегенерат'
        }
      ],
      tableMode: 'SingleSelect',
      recsURL: '/api/v1/admins/users/',
      recAddURL: '/api/v1/admins/events_form_new/',
      recEditURL: '/api/v1/admins/events_form_edit/',
      recDeleteURL: '/api/v1/admins/events_form_delete/',
      searchRow: true,
      changeShowFields: true,
      colCount: 4,
      activeRow: 'Active',
      addButton: false,
      tableColumns: [
        {name: 'ID объекта', alias: 'object_id', whiteSpace: 'nowrap'},
        {name: 'Фамилия', alias: 'surname', whiteSpace: 'nowrap'},
        {name: 'Имя', alias: 'name', whiteSpace: 'nowrap'},
        {name: 'Отчество', alias: 'patronymic', whiteSpace: 'nowrap'},
        {name: 'Роль', alias: 'role', whiteSpace: 'nowrap'},
        {name: 'Дата рождения', alias: 'birthday', whiteSpace: 'nowrap'},
        {name: 'Возраст (полных лет)', alias: 'age', whiteSpace: 'nowrap'},
        {name: 'Пол', alias: 'sex', whiteSpace: 'nowrap'},
        {name: 'Email', alias: 'email', whiteSpace: 'nowrap'},
        {name: 'Телефон', alias: 'phone', whiteSpace: 'nowrap'},
        {name: 'Полное наименование ОО', alias: 'oo_fullname', whiteSpace: 'normal'},
        {name: 'Краткое наименование ОО', alias: 'oo_shortname', whiteSpace: 'normal'},
        {name: 'Государство', alias: 'state', whiteSpace: 'nowrap'}
      ],
      fieldsArray: [],
      selectedProfile: {},
      profileChangeError: ''
    }
  },
  methods: {
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
            this.states=[{id: 0, name: ''}]
            data.states.map((state, id) => {
              this.states.push({id: id+1, name: state.name})
            })
            this.fieldsArray = [
                {
                  ui: 'None',
                  field: 'object_id',
                },
                {
                  ui: 'input',
                  type: 'Text',
                  field: 'surname',
                  add_required: true
                },
                {
                  ui: 'input',
                  type: 'Text',
                  field: 'name',
                  add_required: true
                },
                {
                  ui: 'input',
                  type: 'Text',
                  field: 'patronymic',
                  add_required: true
                },
                {
                  ui: 'select',
                  options: [
                    {
                      id: 0,
                      name: ''
                    },
                    {
                      id: 1,
                      name: 'Администраторы'
                    },
                    {
                      id: 2,
                      name: 'Преподаватели'
                    },
                    {
                      id: '3',
                      name: 'Участники'
                    }
                  ],
                  field: 'role',
                  add_required: true
                },
                {
                  ui: 'date_picker',
                  field: 'birthday',
                  add_required: true
                },
                {
                  ui: 'input',
                  type: 'Number',
                  field: 'age',
                  add_required: false
                },
                {
                  ui: 'switch',
                  field: 'sex',
                  add_required: false
                },
                {
                  ui: 'input',
                  type: 'Email',
                  field: 'email',
                  add_required: true
                },
                {
                  ui: 'input',
                  type: 'Phone',
                  field: 'phone',
                  add_required: true
                },
                {
                  ui: 'input',
                  type: 'Text',
                  field: 'oo_fullname',
                  add_required: true
                },
                {
                  ui: 'input',
                  type: 'Text',
                  field: 'oo_shortname',
                  add_required: true
                },
                {
                  ui: 'select',
                  options: this.states,
                  field: 'state',
                  add_required: true
                },
                {
                  ui: 'icon',
                  field: 'actions'
                }
            ]
            this.$refs.baseComponent.useLoader()
          })
    },
    showUserProfile(object) {
      this.selectedProfile = object
      this.$refs.profileDialog.show()
    },
    async checkUniqueData() {
      this.profileChangeError = ''
      if (this.$refs.profile_form.$refs.profile_phone.componentPhoneField.length !== 18) {
        this.profileChangeError = 'Некорректный формат номера телефона'
        return false
      }
      let date_birth = convertToJSDate(this.$refs.profile_form.$refs.profile_birthday.value)
      let age = Math.floor((new Date() - new Date(date_birth).getTime()) / 3.15576e+10)
      let data = {
        'object_id': this.selectedProfile.object_id,
        'state': this.$refs.profile_form.$refs.profile_state.selectedOption.innerText,
        'surname': this.$refs.profile_form.$refs.profile_surname.value,
        'name': this.$refs.profile_form.$refs.profile_name.value,
        'patronymic': this.$refs.profile_form.$refs.profile_patronymic.value,
        'sex': this.$refs.profile_form.$refs.profile_sex._state.checked,
        'birthday': this.$refs.profile_form.$refs.profile_birthday.value,
        'age': age,
        'email': this.$refs.profile_form.$refs.profile_email.value,
        'phone': this.$refs.profile_form.$refs.profile_phone.componentPhoneField,
        'oo_fullname': '',
        'oo_shortname': ''
      }
      if (this.$refs.profile_form.$refs.profile_role.selectedOption.innerText === 'Администраторы') {
        data.role = 'Администраторы'
      } else {
        data.role = this.$refs.profile_form.$refs.profile_role.selectedOption.innerText
      }
      if (this.$refs.profile_form.$refs.profile_role.selectedOption.innerText === 'Преподаватели') {
        data.oo_fullname = this.$refs.profile_form.$refs.profile_oo_fullname.value
        data.oo_shortname = this.$refs.profile_form.$refs.profile_oo_shortname.value
      }
      this.$refs.baseComponent.useLoader()
      let that = this
      apiRequest(
          this.$store.state.backendUrl+'/api/v1/admins/user_check_phone/',
          'POST',
          true,
          {
            'phone': this.$refs.profile_form.$refs.profile_phone.componentPhoneField,
            'object_id': this.selectedProfile.object_id
          },
          false,
          true
      )
          .then(async function(response) {
            if (response.status !== 200) {
              that.profileChangeError = 'Указанный номер телефона уже использован'
              that.$refs.baseComponent.useLoader()
              return false
            } else {
              apiRequest(
                  that.$store.state.backendUrl+'/api/v1/admins/user_check_email/',
                  'POST',
                  true,
                  {
                    'email': that.$refs.profile_form.$refs.profile_email.value,
                    'object_id': that.selectedProfile.object_id
                  },
                  false,
                  true
              )
                  .then(async function(response) {
                    if (response.status !== 200) {
                      that.profileChangeError = 'Указанный email уже использован'
                      that.$refs.baseComponent.useLoader()
                    } else {
                      await that.profileChange(data)
                    }
                  })
            }
          })
    },
    async profileChange(data) {
      apiRequest(
          this.$store.state.backendUrl+'/api/v1/admins/user_edit/',
          'POST',
          true,
          data,
          false,
          false
      )
          .then(data => {
            if (data['error']) {
              showMessage('error', data['error'])
            } else {
              showMessage('success', data['success'])
            }
            this.$refs.profileDialog.close()
            this.$refs.pagination_table.getRecs(
                (this.$refs.pagination_table.pageNumber-1)*this.$refs.pagination_table.recCount,
                this.$refs.pagination_table.recCount
            )
            this.$refs.baseComponent.useLoader()
          })
    },
    async changePassword() {
      if (this.$refs.profile_form.$refs.password1.passwordStr.length < 8) {
        this.$refs.profile_form.$refs.password1.valueState = 'Error'
        this.$refs.profile_form.$refs.password1.valueStateText = 'Минимальная длина пароля - 8 символов'
        return false
      } else {
        this.$refs.profile_form.$refs.password1.valueState = 'None'
      }
      if (this.$refs.profile_form.$refs.password1.passwordStr !== this.$refs.profile_form.$refs.password2.passwordStr) {
        this.$refs.profile_form.$refs.password1.valueState = 'Error'
        this.$refs.profile_form.$refs.password2.valueState = 'Error'
        this.$refs.profile_form.$refs.password1.valueStateText = 'Введенные пароли не совпадают'
        this.$refs.profile_form.$refs.password2.valueStateText = 'Введенные пароли не совпадают'
        return false
      } else {
        this.$refs.profile_form.$refs.password1.valueState = 'None'
        this.$refs.profile_form.$refs.password2.valueState = 'None'
      }
      let password = this.$refs.profile_form.$refs.password1.passwordStr
      this.$refs.profile_form.$refs.passwordPopover.close()
      this.$refs.baseComponent.useLoader()
      apiRequest(
          this.$store.state.backendUrl+'/api/v1/admins/user_change_password/',
          'POST',
          true,
          {
            'password': password,
            'object_id': this.selectedProfile.object_id
          },
          false,
          false
      )
          .then(data => {
            if (data['error']) {
              showMessage('error', data['error'])
            } else {
              showMessage('success', data['success'])
            }
            this.$refs.profileDialog.close()
            this.$refs.baseComponent.useLoader()
          })
    },
  },
  mounted() {
    this.$refs.baseComponent.useLoader()
    this.getStates()
  }
}
</script>

<style scoped>

</style>