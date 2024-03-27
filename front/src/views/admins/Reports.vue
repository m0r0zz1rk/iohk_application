<template>
  <LkBase ref="baseComponent">
    <slot>
      <ui5-card class="full-card">
        <ui5-card-header slot="header"
                         title-text="Отчеты">
        </ui5-card-header>
        <ui5-tabcontainer fixed collapsed @tab-select="e => changeTab(e.detail.tabIndex)">
          <ui5-tab text="Выгрузка заявок" :selected="selectedTab === 'apps'" />
          <ui5-tab text="Количественный отчет" :selected="selectedTab === 'counts'" />
        </ui5-tabcontainer><br/><br/>
        <div v-if="selectedTab === 'apps'" style="display: flex; justify-content: center;">
          <ui5-table class="criteria_table" sticky-column-header>
            <ui5-table-column slot="columns">Критерий</ui5-table-column>
            <ui5-table-column slot="columns" style="width: 75%;">Значение</ui5-table-column>
            <ui5-table-row>
              <ui5-table-cell style="text-align: right">Мероприятие:</ui5-table-cell>
              <ui5-table-cell>
                <PaginationTable v-bind:tableMode="'SingleSelect'"
                                 v-bind:recsURL="'/api/v1/reports/events/list/'"
                                 v-bind:searchRow="true"
                                 v-bind:colCount="8"
                                 v-bind:activeRow="'Active'"
                                 v-bind:activeRowEvent="selectEvent"
                                 v-bind:addButton="false"
                                 v-bind:tableColumns="[
                                    {name: 'ID объекта', alias: 'object_id', whiteSpace: 'nowrap'},
                                    {name: 'Мероприятие', alias: 'name', whiteSpace: 'normal'},
                                    {name: 'Сроки проведения', alias: 'date_range', whiteSpace: 'normal'},
                                    {name: 'Статус', alias: 'event_status', whiteSpace: 'nowrap'}
                                 ]"
                                 v-bind:fieldsArray="[
                                     {
                                       ui: 'None',
                                       field: 'object_id'
                                     },
                                     {
                                       ui: 'input',
                                       type: 'Text',
                                       field: 'name'
                                     },
                                     {
                                       ui: 'date_range_picker',
                                       field: 'date_range'
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
                                          name: 'Создано'
                                        },
                                        {
                                          id: 2,
                                          name: 'Опубликовано'
                                        },
                                        {
                                          id: 3,
                                          name: 'Отменено'
                                        },
                                        {
                                          id: 4,
                                          name: 'В процессе'
                                        },
                                        {
                                          id: 5,
                                          name: 'Снято с публикации'
                                        }
                                      ],
                                      field: 'event_status',
                                      add_required: false
                                    }
                                 ]"
                                 v-bind:dataTableHeight="35"
                />
              </ui5-table-cell>
            </ui5-table-row>
            <ui5-table-row>
              <ui5-table-cell style="text-align: right">Типы заявок в отчете:</ui5-table-cell>
              <ui5-table-cell>
                <ui5-select ref="apps_types_select">
                  <ui5-option value="user">Заявки пользователей</ui5-option>
                  <ui5-option value="part">Заявки участников от пользователей</ui5-option>
                  <ui5-option value="all">Все заявки</ui5-option>
                </ui5-select>
              </ui5-table-cell>
            </ui5-table-row>
            <ui5-table-row>
              <ui5-table-cell style="text-align: right">Выгрузить:</ui5-table-cell>
              <ui5-table-cell>
                <ui5-button v-if="!(appsProcess)"
                            @click="e => appsDownload()">
                  Выгрузка
                </ui5-button>
                <ui5-message-strip v-if="appsProcess" design="Warning" hideCloseButton>
                  <img src="/src/assets/loading.gif"
                       alt=""
                       width="16"
                       height="16"
                       slot="icon">
                  Подождите, идет формирование файла...
                </ui5-message-strip>
              </ui5-table-cell>
            </ui5-table-row>
          </ui5-table>
        </div>
        <div v-if="selectedTab === 'counts'" class="counts-report-div">
          <ui5-table class="criteria_table" sticky-column-header>
            <ui5-table-column slot="columns">Критерий</ui5-table-column>
            <ui5-table-column slot="columns" style="width: 75%;">Значение</ui5-table-column>
            <ui5-table-row>
              <ui5-table-cell style="text-align: right">Мероприятия:</ui5-table-cell>
              <ui5-table-cell>
                <PaginationTable ref="events_table" v-bind:tableMode="'None'"
                                 v-bind:recsURL="'/api/v1/reports/events/list/'"
                                 v-bind:searchRow="true"
                                 v-bind:colCount="8"
                                 v-bind:activeRow="'Inactive'"
                                 v-bind:addButton="false"
                                 v-bind:tableColumns="[
                                    {name: 'checkbox', alias: 'checkbox', whiteSpace: 'nowrap'},
                                    {name: 'ID объекта', alias: 'object_id', whiteSpace: 'nowrap'},
                                    {name: 'Мероприятие', alias: 'name', whiteSpace: 'normal'},
                                    {name: 'Сроки проведения', alias: 'date_range', whiteSpace: 'normal'},
                                    {name: 'Статус', alias: 'event_status', whiteSpace: 'nowrap'}
                                 ]"
                                 v-bind:fieldsArray="[
                                     {
                                       ui: 'None',
                                       field: 'object_id'
                                     },
                                     {
                                       ui: 'None',
                                       field: 'checkbox'
                                     },
                                     {
                                       ui: 'input',
                                       type: 'Text',
                                       field: 'name'
                                     },
                                     {
                                       ui: 'date_range_picker',
                                       field: 'date_range'
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
                                          name: 'Создано'
                                        },
                                        {
                                          id: 2,
                                          name: 'Опубликовано'
                                        },
                                        {
                                          id: 3,
                                          name: 'Отменено'
                                        },
                                        {
                                          id: 4,
                                          name: 'В процессе'
                                        },
                                        {
                                          id: 5,
                                          name: 'Снято с публикации'
                                        }
                                      ],
                                      field: 'event_status',
                                      add_required: false
                                    }
                                 ]"
                                 v-bind:dataTableHeight="35"
                />
              </ui5-table-cell>
            </ui5-table-row>
            <ui5-table-row>
              <ui5-table-cell style="text-align: right">Типы заявок в отчете:</ui5-table-cell>
              <ui5-table-cell>
                <ui5-select ref="count_types_select">
                  <ui5-option value="user">Заявки пользователей</ui5-option>
                  <ui5-option value="part">Заявки участников от пользователей</ui5-option>
                  <ui5-option value="all">Все заявки</ui5-option>
                </ui5-select>
              </ui5-table-cell>
            </ui5-table-row>
            <ui5-table-row>
              <ui5-table-cell style="text-align: right">Фильтры:</ui5-table-cell>
              <ui5-table-cell>
                <ui5-table id="filters-table" sticky-column-header>
                  <ui5-table-column>№</ui5-table-column>
                  <ui5-table-column>Наименование поля</ui5-table-column>
                  <ui5-table-column>Значение</ui5-table-column>
                  <ui5-table-column>Действия</ui5-table-column>
                  <ui5-table-row>
                    <ui5-table-cell class="additional-row-cell">
                      <ui5-icon name="add" style="color: white" />
                    </ui5-table-cell>
                    <ui5-table-cell class="additional-row-cell">
                      <ui5-textarea ref="filter_add_field" />
                    </ui5-table-cell>
                    <ui5-table-cell class="additional-row-cell">
                      <ui5-textarea ref="filter_add_value" />
                    </ui5-table-cell>
                    <ui5-table-cell class="additional-row-cell">
                      <ui5-icon name="accept"
                                interactive
                                style="color: white"
                                @click="e => addFilter()"/>
                    </ui5-table-cell>
                  </ui5-table-row>
                  <ui5-table-row v-for="filter in filtersArray">
                    <ui5-table-cell>{{filter.id}}</ui5-table-cell>
                    <ui5-table-cell>{{filter.field}}</ui5-table-cell>
                    <ui5-table-cell>{{filter.value}}</ui5-table-cell>
                    <ui5-table-cell>
                      <ui5-icon name="delete" interactive @click="e => deleteFilter(filter)" />
                    </ui5-table-cell>
                  </ui5-table-row>
                </ui5-table>
              </ui5-table-cell>
            </ui5-table-row>
            <ui5-table-row>
              <ui5-table-cell style="text-align: right">Итоговая строка:</ui5-table-cell>
              <ui5-table-cell>
                <ui5-switch ref="total_row_switch" />
              </ui5-table-cell>
            </ui5-table-row>
            <ui5-table-row>
              <ui5-table-cell style="text-align: right">Фомирование:</ui5-table-cell>
              <ui5-table-cell>
                <ui5-button icon="excel-attachment" v-if="!(countProcess)"
                            @click="e => countDownload()">
                  Сформировать отчет
                </ui5-button>
                <ui5-message-strip v-if="countProcess" design="Warning" hideCloseButton>
                  <img src="/src/assets/loading.gif"
                       alt=""
                       width="16"
                       height="16"
                       slot="icon">
                  Подождите, идет формирование файла...
                </ui5-message-strip>
              </ui5-table-cell>
            </ui5-table-row>
          </ui5-table>
        </div>
      </ui5-card>
    </slot>
  </LkBase>
</template>

<script>

import LkBase from "../../components/LkBase.vue";
import PaginationTable from "../../components/tables/PaginationTable.vue";
import {apiRequest} from "../../additional/functions/api_request.js";
import {changeTableView} from "../../additional/functions/additional.js";
import {showMessage} from "../../additional/functions/message-strips.js";

export default {
  name: 'Reports',
  components: {PaginationTable, LkBase},
  data() {
    return {
      appsProcess: false,
      countProcess: false,
      selectedTab: 'apps',
      selectedEvent: {
        id: '',
        name: ''
      },
      filtersArray: []
    }
  },
  methods: {
    init() {
      setTimeout(changeTableView, 25)
    },
    changeTab(tab_index) {
      switch (tab_index) {
        case 0:
          this.selectedTab = 'apps'
          break

        default:
          this.selectedTab = 'counts'
          setTimeout(() => {
            document.querySelector('#filters-table').shadowRoot.querySelector('.ui5-table-header-row').remove()
          }, 25)
      }
      this.init()
    },
    selectEvent(row) {
      this.selectedEvent['id'] = row.object_id
      this.selectedEvent['name'] = row.name
    },
    async appsDownload() {
      if (this.selectedEvent['id'].length === 0) {
        showMessage('error', 'Выберите мероприятие')
        return false
      }
      let data = {
        'event_id': this.selectedEvent['id'],
        'apps_types': this.$refs.apps_types_select.selectedOption.value
      }
      this.appsProcess = true
      apiRequest(
          '/api/v1/reports/apps_report/',
          'POST',
          true,
          data,
          false,
          true
      )
          .then(resp => {
            if (resp.status === 200) {
              return resp.blob()
            } else {
              showMessage('error', 'Произошла ошибка при генерации отчета. Повторите попытку позже')
              this.appsProcess = false
              return false
            }
          })
          .then(blob => {
            let a = document.createElement('a')
            a.href = window.URL.createObjectURL(blob)
            a.download = this.selectedEvent['name']+'.xlsx'
            a.click()
            showMessage('success', 'Отчет успешно сформирован')
            this.appsProcess = false
          })
    },
    addFilter() {
      if ((this.$refs.filter_add_field.value.length === 0) ||
          (this.$refs.filter_add_value.value.length === 0)) {
        showMessage('error', 'Заполните поля таблицы фильтров')
        return false
      }
      this.filtersArray.push({
        'id': this.filtersArray.length + 1,
        'field': this.$refs.filter_add_field.value,
        'value': this.$refs.filter_add_value.value
      })
    },
    deleteFilter(filter) {
      let index = this.filtersArray.indexOf(filter)
      this.filtersArray.splice(index, 1)
    },
    async countDownload() {
      let events = this.$refs.events_table.checkBoxRecs
      if (events.length === 0) {
        showMessage('error', 'Выберите мероприятия')
        return false
      }
      let events_list = []
      events.map((event, id) => {
        events_list.push({
          'id': id+1,
          'event_id': event
        })
      })
      let data = {
        'events': events_list,
        'apps_types': this.$refs.count_types_select.selectedOption.value,
        'filters': this.filtersArray,
        'total_row': this.$refs.total_row_switch._state.checked
      }
      this.countProcess = true
      apiRequest(
          '/api/v1/reports/count_report/',
          'POST',
          true,
          data,
          false,
          true
      )
          .then(resp => {
            if (resp.status === 200) {
              return resp.blob()
            } else {
              showMessage('error', 'Произошла ошибка при генерации отчета. Повторите попытку позже')
              this.appsProcess = false
              return false
            }
          })
          .then(blob => {
            let a = document.createElement('a')
            a.href = window.URL.createObjectURL(blob)
            a.download = 'Количественный отчет.xlsx'
            a.click()
            showMessage('success', 'Отчет успешно сформирован')
            this.countProcess = false
          })
    }
  },
  mounted() {
    this.init()
  }
}

</script>


<style scoped>
  .criteria_table{
    width: 90%;
  }
  .counts-report-div{
    display: flex;
    justify-content: center;
    height: 70vh;
    overflow: auto;
  }
</style>