<template>
  <LkBase ref="baseComponent">
    <slot>
      <ui5-card class="full-card">
        <ui5-card-header slot="header"
                         title-text="Журнал АИС">
        </ui5-card-header>
        <div style="height:  80vh">
          <PaginationTable v-bind:recsURL="recsURL"
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
import PaginationTable from "../../components/tables/PaginationTable.vue";
import LkBase from "../../components/LkBase.vue";
import journalEventResult from "../../additional/consts/journal_event_results.js";
import journalRecTypes from "../../additional/consts/journal_rec_types.js";

export default {
  name: 'Journal',
  components: {LkBase, PaginationTable},
  data() {
    return {
      eventResults: [],
      recTypes: [],
      dataTableHeight: 68,
      recsURL: '/api/v1/admins/journal/',
      searchRow: true,
      changeShowFields: true,
      colCount: 8,
      activeRow: 'Inactive',
      addButton: false,
      tableColumns: [
        {name: 'ID объекта', alias: 'object_id', whiteSpace: 'nowrap'},
        {name: 'Время события', alias: 'event_time', whiteSpace: 'nowrap'},
        {name: 'Субъект', alias: 'source', whiteSpace: 'nowrap'},
        {name: 'Тип события', alias: 'rec_type', whiteSpace: 'nowrap'},
        {name: 'Статус события', alias: 'event_result', whiteSpace: 'nowrap'},
        {name: 'Детали', alias: 'description', whiteSpace: 'normal'},
      ],
      fieldsArray: []
    }
  },
  mounted() {
    this.$refs.baseComponent.useLoader()
    this.eventResults = [{id: 0, type: '', name: ''}]
    this.recTypes = [{id: 0, type: '', name: ''}]
    journalEventResult.map((res) => {
      this.eventResults.push(res)
    })
    journalRecTypes.map((type) => {
      this.recTypes.push(type)
    })
    this.fieldsArray = [
      {
        ui: 'None',
        field: 'object_id',
      },
      {
        ui: 'date_picker',
        field: 'event_time',
        add_required: false,
      },
      {
        ui: 'input',
        type: 'Text',
        field: 'source',
        add_required: false
      },
      {
        ui: 'select',
        options: this.recTypes,
        field: 'rec_type',
        add_required: false
      },
      {
        ui: 'select',
        options: this.eventResults,
        field: 'event_result',
        add_required: false
      },
      {
        ui: 'input',
        type: 'Text',
        field: 'description',
        add_required: false
      },
    ]
    this.$refs.baseComponent.useLoader()
  }
}
</script>

<style scoped>

</style>