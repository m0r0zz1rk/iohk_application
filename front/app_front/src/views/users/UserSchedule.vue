<template>
  <LkBase ref="baseComponent">
    <slot>
      <ui5-card class="full-card">
        <ui5-card-header slot="header"
                         title-text="Расписание ближайших занятий">
        </ui5-card-header>
        <div style="height:  80vh">
          <PaginationTable v-bind:tableMode="'None'"
                           v-bind:recsURL="'/api/v1/users/schedule/'"
                           v-bind:searchRow="false"
                           v-bind:colCount="8"
                           v-bind:activeRow="'InActive'"
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

import PaginationTable from "../../components/tables/PaginationTable.vue";
import LkBase from "../../components/LkBase.vue";

export default {
  name: 'UserSchedule',
  components: {LkBase, PaginationTable},
  data() {
    return {
      fieldsArray: [
        {
          ui: 'None',
          field: 'object_id',
        },
        {
          ui: 'datetime_picker',
          field: 'start',
          add_required: false
        },
        {
          ui: 'datetime_picker',
          field: 'end',
          add_required: false
        },
        {
          ui: 'input',
          type: 'Text',
          field: 'theme',
          add_required: false
        },
        {
          ui: 'input',
          type: 'Text',
          field: 'form',
          add_required: false
        },
        {
          ui: 'input',
          type: 'Text',
          field: 'url',
          add_required: false
        },
        {
          ui: 'input',
          type: 'Text',
          field: 'address',
          add_required: false
        },
      ],
      tableColumns: [
        {name: 'ID объекта', alias: 'object_id', whiteSpace: 'nowrap'},
        {name: 'Начало', alias: 'start', whiteSpace: 'nowrap'},
        {name: 'Окончание', alias: 'end', whiteSpace: 'nowrap'},
        {name: 'Тема', alias: 'theme', whiteSpace: 'nowrap'},
        {name: 'Форма', alias: 'form', whiteSpace: 'normal'},
        {name: 'Ссылка', alias: 'url', whiteSpace: 'normal'},
        {name: 'Адрес проведения', alias: 'address', whiteSpace: 'nowrap'}
      ],
    }
  }
}

</script>


<style scoped>

</style>