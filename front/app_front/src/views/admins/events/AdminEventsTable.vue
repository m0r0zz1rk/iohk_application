<template>
    <ui5-card class="full-card">
      <ui5-card-header slot="header"
                       :title-text="headerText">
      </ui5-card-header>
      <div style="height:  80vh">
        <PaginationTable v-if="this.fieldsArray.length > 0"
                         v-bind:tableMode="tableMode"
                         v-bind:recsURL="recsURL"
                         v-bind:recAddURL="recAddURL"
                         v-bind:recEditURL="recEditURL"
                         v-bind:recDeleteURL="recDeleteURL"
                         v-bind:searchRow="searchRow"
                         v-bind:changeShowFields="changeShowFields"
                         v-bind:colCount="colCount"
                         v-bind:activeRow="activeRow"
                         v-bind:activeRowEvent="activeRowEvent"
                         v-bind:addButton="addButton"
                         v-bind:tableColumns="tableColumns"
                         v-bind:fieldsArray="fieldsArray"
                         v-bind:dataTableHeight="dataTableHeight"
        />
      </div>
    </ui5-card>
</template>

<script>
import PaginationTable from "../../../components/PaginationTable.vue";

export default {
  name: 'AdminEventsTable',
  components: {PaginationTable},
  props: {
    headerText: {type: String},
    tableMode: {type: String},
    tableColumns: {type: Array},
    showActions: {type: Boolean},
    addButton: {type: Boolean},
    activeRow: {type: String},
    activeRowEvent: {type: Function}
  },
  data() {
    return {
      dataTableHeight: 68,
      recsURL: '/api/v1/admins/events/',
      recAddURL: '/api/v1/admins/event_new/',
      recEditURL: '/api/v1/admins/event_edit/',
      recDeleteURL: '/api/v1/admins/event_delete/',
      searchRow: true,
      changeShowFields: true,
      colCount: 4,
      addButton: true,
      fieldsArray: [],
      types: [
        {
          id: 0,
          name: ''
        }
      ],
      categories: [
        {
          id: 0,
          name: ''
        }
      ]
    }
  },
  methods: {
    async getEventTypesAndCats() {
      let that = this
      await fetch(this.$store.state.backendUrl + '/api/v1/admins/events_types/', {
        method: 'GET',
        headers: {
          'X-CSRFToken': getCookie("csrftoken"),
          'Content-Type': 'application/json;charset=UTF-8',
          'Authorization': 'Token ' + getCookie('iohk_token')
        },
      })
          .then(resp => {
            if (resp.status === 200) {
              return resp.json()
            } else {
              showMessage('error', 'Произошла ошибка при получении типов мероприятий, повторите попытку позже')
              return false
            }
          })
          .then(data => {
            data.map((type, id) => {
              this.types.push({id: id + 1, name: type.name})
            })
            fetch(this.$store.state.backendUrl + '/api/v1/admins/participant_categories/', {
              method: 'GET',
              headers: {
                'X-CSRFToken': getCookie("csrftoken"),
                'Content-Type': 'application/json;charset=UTF-8',
                'Authorization': 'Token ' + getCookie('iohk_token')
              },
            })
                .then(resp => {
                  if (resp.status === 200) {
                    return resp.json()
                  } else {
                    showMessage('error', 'Произошла ошибка при получении категорий участников, повторите попытку позже')
                    return false
                  }
                })
                .then(data => {
                  data.map((category, id) => {
                    that.categories.push({id: id + 1, name: category.name})
                  })
                  this.fieldsArray = [
                    {
                      ui: 'None',
                      field: 'object_id',
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
                      field: 'description',
                      add_required: false
                    },
                    {
                      ui: 'select',
                      options: that.types,
                      field: 'event_type',
                      add_required: true
                    },
                    {
                      ui: 'date_range_picker',
                      field: 'app_date_range',
                      add_required: true
                    },
                    {
                      ui: 'date_range_picker',
                      field: 'date_range',
                      add_required: true
                    },
                    {
                      ui: 'multiple',
                      options: that.categories,
                      field: 'categories',
                      add_required: true
                    }

                  ]
                  if (this.showActions) {
                    this.fieldsArray.push(
                        {
                          ui: 'icon',
                          field: 'actions'
                        }
                    )
                  }
                })
          })
    }
  },
  mounted() {
    this.getEventTypesAndCats()
  }
}
</script>

<style scoped>

</style>