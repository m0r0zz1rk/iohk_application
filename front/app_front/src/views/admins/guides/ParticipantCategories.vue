<template>
  <div style="height:  70vh">
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

</template>

<script>
import PaginationTable from "../../../components/PaginationTable.vue";

export default {
  name: 'ParticipantCategories',
  components: {PaginationTable},
  data() {
    return {
      dataTableHeight: 60,
      recsURL: '/api/v1/admins/participant_categories/',
      recAddURL: '/api/v1/admins/participant_category_new/',
      recEditURL: '/api/v1/admins/participant_category_edit/',
      recDeleteURL: '/api/v1/admins/participant_category_delete/',
      searchRow: true,
      changeShowFields: true,
      colCount: 4,
      activeRow: 'Inactive',
      addButton: true,
      tableColumns: [
        {name: 'ID объекта', alias: 'object_id', whiteSpace: 'nowrap'},
        {name: 'Наименование', alias: 'name', whiteSpace: 'nowrap'},
        {name: 'Роль пользователей', alias: 'group', whiteSpace: 'nowrap'},
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
          field: 'name',
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
              name: 'Преподаватели',
            },
            {
              id: 2,
              name: 'Участники'
            }
          ],
          field: 'group',
          add_required: true
        },
        {
          ui: 'icon',
          field: 'actions'
        }
      ]
    }
  }
}
</script>

<style scoped>

</style>