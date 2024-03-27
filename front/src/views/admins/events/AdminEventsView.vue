<template>
  <LkBase ref="baseComponent">
    <slot>
      <AdminEventsTable v-bind:tableColumns="tableColumns"
                        v-bind:headerText="'Просмотр мероприятий'"
                        v-bind:addButton="true"
                        v-bind:activeRow="true"
                        v-bind:showActions="true"/>
    </slot>
  </LkBase>
</template>

<script>
import LkBase from "../../../components/LkBase.vue";
import PaginationTable from "../../../components/tables/PaginationTable.vue";
import AdminEventsTable from "./AdminEventsTable.vue";

export default {
  name: 'AdminEventsView',
  components: {AdminEventsTable, LkBase, PaginationTable},
  data() {
    return {
      tableColumns: [
        {name: 'ID объекта', alias: 'object_id', whiteSpace: 'nowrap'},
        {name: 'Наименование', alias: 'name', whiteSpace: 'break-spaces'},
        {name: 'Краткое пояснение', alias: 'description', whiteSpace: 'normal'},
        {name: 'Тип', alias: 'event_type', whiteSpace: 'nowrap'},
        {name: 'Статус', alias: 'event_status', whiteSpace: 'normal'},
        {name: 'Сроки подачи заявок', alias: 'app_date_range', whiteSpace: 'nowrap'},
        {name: 'Сроки проведения мероприятия', alias: 'date_range', whiteSpace: 'nowrap'},
        {name: 'Категории участников', alias: 'categories', whiteSpace: 'nowrap'},
        {name: 'Действия', alias: 'actions'}
      ],
    }
  }
}
</script>

<style scoped>

</style>