<template>
  <LkBase ref="baseComponent">
    <slot>
      <ui5-card class="full-card">
        <ui5-card-header slot="header"
                         title-text="Заявки">
        </ui5-card-header>
        <div style="height:  80vh">
          <PaginationTable v-if="this.fieldsArray.length > 0"
                           v-bind:tableMode="'SingleSelect'"
                           v-bind:recsURL="'/api/v1/admins/apps/list/'"
                           v-bind:searchRow="true"
                           v-bind:colCount="8"
                           v-bind:activeRow="'Active'"
                           v-bind:activeRowEvent="openApp"
                           v-bind:addButton="false"
                           v-bind:tableColumns="tableColumns"
                           v-bind:fieldsArray="fieldsArray"
                           v-bind:dataTableHeight="68"
          />
        </div>
      </ui5-card>
    </slot>
  </LkBase>
</template>

<script>

import PaginationTable from "../../../components/tables/PaginationTable.vue";
import LkBase from "../../../components/LkBase.vue";
import {apiRequest} from "../../../additional/functions/api_request.js";

export default {
  name: 'AdminApps',
  components: {LkBase, PaginationTable},
  data() {
    return {
      fieldsArray: [],
      tableColumns: [
        {name: 'ID объекта', alias: 'object_id', whiteSpace: 'nowrap'},
        {name: 'Дата подачи', alias: 'date_create', whiteSpace: 'nowrap'},
        {name: 'ФИО пользователя', alias: 'fio', whiteSpace: 'nowrap'},
        {name: 'Тип мероприятия', alias: 'event_type', whiteSpace: 'nowrap'},
        {name: 'Мероприятие', alias: 'event_name', whiteSpace: 'normal'},
        {name: 'Сроки проведения', alias: 'event_date_range', whiteSpace: 'normal'},
        {name: 'Статус', alias: 'app_status', whiteSpace: 'nowrap'}
      ],
    }
  },
  methods: {
    init() {
      apiRequest(
          this.$store.state.backendUrl+'/api/v1/users/event_types/',
          'GET',
          true,
          null,
          false,
          false
      )
          .then(data => {
            let types = []
            data.map((type) => {
              types.push({
                id: type.object_id,
                name: type.name
              })
            })
            this.fieldsArray = [
              {
                ui: 'None',
                field: 'object_id',
              },
              {
                ui: 'date_picker',
                field: 'date_create',
                add_required: false
              },
              {
                ui: 'input',
                type: 'Text',
                field: 'fio',
                add_required: false
              },
              {
                ui: 'select',
                options: [
                  {
                    id: 0,
                    name: ''
                  },
                  ...types
                ],
                field: 'event_type',
                add_required: false
              },
              {
                ui: 'input',
                type: 'Text',
                field: 'event_name',
                add_required: false
              },
              {
                ui: 'date_range_picker',
                field: 'event_date_range',
                add_required: false
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
                    name: 'Черновик'
                  },
                  {
                    id: 2,
                    name: 'Сохранена'
                  },
                  {
                    id: 3,
                    name: 'Отправлена'
                  },
                  {
                    id: 4,
                    name: 'Принята'
                  },
                  {
                    id: 5,
                    name: 'Отклонена'
                  },
                  {
                    id: 6,
                    name: 'Отозвана'
                  },
                ],
                field: 'app_status',
                add_required: false
              }
            ]
          })
    },
    openApp(row) {
      this.$router.push('/apps/admin_app_detail/'+row.object_id+'/')
    }
  },
  mounted() {
    this.init()
  }
}

</script>

<style scoped>

</style>