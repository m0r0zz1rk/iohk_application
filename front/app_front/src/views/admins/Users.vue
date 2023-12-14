<template>
  <LkBase ref="baseComponent">
    <slot>
      <ui5-card class="full-card">
        <ui5-card-header slot="header"
                         title-text="Пользователи">
        </ui5-card-header>
        <div style="height:  80vh">
          <PaginationTable v-bind:recsURL="recsURL"
                           v-bind:recAddURL="recAddURL"
                           v-bind:recEditURL="recEditURL"
                           v-bind:recDeleteURL="recDeleteURL"
                           v-bind:searchRow="searchRow"
                           v-bind:changeShowFields="changeShowFields"
                           v-bind:colCount="colCount"
                           v-bind:activeRow="activeRow"
                           v-bind:addButton="addButton"
                           v-bind:tableColumns="tableColumns"
                           v-bind:fieldsArray="fieldsArray"
                           v-bind:dataTableHeight="dataTableHeight"
          />
        </div>
      </ui5-card>
    </slot>
  </LkBase>

</template>

<script>
import PaginationTable from "../../components/PaginationTable.vue";
import LkBase from "../../components/LkBase.vue";

export default {
  name: 'Users',
  components: {LkBase, PaginationTable},
  data() {
    return {
      dataTableHeight: 68,
      states: [],
      recsURL: '/api/v1/admins/users',
      recAddURL: '/api/v1/admins/events_form_new/',
      recEditURL: '/api/v1/admins/events_form_edit/',
      recDeleteURL: '/api/v1/admins/events_form_delete/',
      searchRow: true,
      changeShowFields: true,
      colCount: 4,
      activeRow: false,
      addButton: true,
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
        {name: 'Государство', alias: 'state', whiteSpace: 'nowrap'},
        {name: 'Действия', alias: 'actions'}
      ],
      fieldsArray: [
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
          type: 'Text',
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
    }
  },
  methods: {
    async getStates() {
      await fetch(this.$store.state.backendUrl+'/api/v1/auth/states/', {
        method: 'GET',
        headers: {
          'X-CSRFToken': getCookie("csrftoken"),
          'Content-Type': 'application/json;charset=UTF-8',
        },
      })
          .then(resp => {
            if (resp.status === 200) {
              return resp.json()
            } else {
              showMessage('error', 'Произошла ошибка при получении списка государств, повторите попытку позже')
              return false
            }
          })
          .then(data => {
            console.log(data.states)
            this.states = data.states
          })
    },
  },
  beforeMount() {
    this.getStates()
  }
}
</script>

<style scoped>

</style>