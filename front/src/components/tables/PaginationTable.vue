<template>
  <div style="margin-left: 4px;">
    <div style="height: 10%">
      <div>
        <div class="upper-table-container">
          <div>
            <div v-if="this.addButton" style="display: inline-block">
              <ui5-button icon="add"
                          @click="action = 'add'; openAddEditDialog()">Добавить</ui5-button>&nbsp
            </div>
            <div v-if="this.changeShowFields" style="display: inline-block">
              <ui5-button
                  icon="screen-split-three" ref="fieldsButton"
                  @click="e => this.$refs.fields_popover.showAt(this.$refs.fieldsButton)">
                Столбцы
              </ui5-button>
              <ui5-popover v-if="this.changeShowFields"
                           placement-type="Right"
                           ref="fields_popover">
                <ui5-multi-combobox style="width: 50vw;"
                                    @selection-change="e => changeFieldView(e.detail.items)">
                  <ui5-mcb-item v-for="item in tableColumns"
                                :text="item.name"
                                :selected="item.alias !== 'object_id'" />
                </ui5-multi-combobox>
              </ui5-popover>
              &nbsp;&nbsp;
            </div>
            <div v-if="this.info" style="display: inline-block">
              <ui5-button
                  icon="information"
                  @click="e => this.$refs.info_popover.showAt(e.target)">
                Справка
              </ui5-button>
              <ui5-popover v-if="this.info" ref="info_popover"
                           placement-type="Right">
                {{infoText}}
              </ui5-popover>
            </div>
          </div>
          <div>
            <div style="display: inline-block">
              Записей на странице:
            </div>&nbsp;
            <div style="display: inline-block">
              <ui5-select @change="e => this.recCount = e.detail.selectedOption.innerText">
                <ui5-option v-for="option in recCountOptions"
                            :selected="option === recCount">{{option}}</ui5-option>
              </ui5-select>
            </div>&nbsp;
          </div>
        </div>
      </div>
    </div>
    <div id="data_table"  :style="{height: dataTableHeight + 'vh'}">
      <ui5-table :busy="tableBusy"
                 :mode="tableMode"
                 sticky-column-header>
        <ui5-table-column slot="columns">№</ui5-table-column>
        <template v-for="col in tableColumns">
          <ui5-table-column v-if="fieldsList.includes(col.alias)"
                            style="white-space: nowrap"
                            slot="columns">
            <div v-if="col.name === 'checkbox'">
              <ui5-checkbox ref="mainCheckBox"
                            @change="checkBoxRecAction('all')" />
            </div>
            <div v-if="col.name !== 'checkbox'">
              {{col.name}}
            </div>
          </ui5-table-column>
        </template>
        <ui5-table-row v-if="searchRow">
          <ui5-table-cell class="find-row-cell">
            <ui5-icon name="search" class="table-icon" />
          </ui5-table-cell>
          <template v-for="obj in fieldsArray">
            <template v-if="obj.ui !== 'icon'">
              <ui5-table-cell v-if="fieldsList.includes(obj.field)"
                              style="white-space: nowrap"
                              class="find-row-cell">
                <p v-if="['None', 'password', 'checkbox', 'app_status'].includes(obj.ui)">-</p>
                <p v-if="obj.ui === 'today'">{{componentGetDay(false)}}</p>
                <template v-if="obj.ui === 'input'">
                  <PhoneField v-if="obj.type === 'Phone'"
                              ref="filter_phone"
                              v-bind:phoneValueState="'None'"
                              v-bind:phoneStateText="''"
                              v-bind:changePhoneAction="filterPhone" />
                  <ui5-input v-if="obj.type !== 'Phone'"
                             :ref="'filter_'+obj.field"
                             :type="obj.type"
                             @change="e => filterRecs(e.target.value, obj.field)" />
                </template>
                <template v-if="obj.ui === 'switch'">
                  <div>
                    <div>
                      <ui5-switch :text-on="obj.field === 'sex' && 'М'"
                                  :ref="'filter_'+obj.field"
                                  :text-off="obj.field === 'sex' && 'Ж'"
                                  @change="e => filterRecs(e.target._state.checked, obj.field)"/>
                    </div>
                    <div>
                      <ui5-icon interactive class="table-filter-icon"
                                name="clear-filter"
                                @click="e => filterRecs('', obj.field)" />
                    </div>
                  </div>
                </template>
                <ui5-select v-if="['select', 'multiple'].includes(obj.ui)"
                            :ref="'filter_'+obj.field"
                            @change="e => filterRecs(e.detail.selectedOption.innerText, obj.field)">
                  <ui5-option v-for="option in obj.options">
                    {{option.name}}
                  </ui5-option>
                </ui5-select>
                <ui5-date-picker v-if="obj.ui === 'date_picker'"
                                 :ref="'filter_'+obj.field"
                                 format-pattern="dd.MM.yyyy"
                                 @change="e => filterRecs(e.target.value, obj.field)" />
                <ui5-datetime-picker v-if="obj.ui === 'datetime_picker'"
                                     :ref="'filter_'+obj.field"
                                     format-pattern="dd.MM.yyyy HH:mm"
                                     @change="e => filterRecs(e.target.value, obj.field)" />
                <ui5-daterange-picker v-if="obj.ui === 'date_range_picker'"
                                      :ref="'filter_'+obj.field"
                                      format-pattern="dd.MM.yyyy"
                                      @change="e => filterRecs(e.target.value, obj.field)"/>
              </ui5-table-cell>
            </template>
            <ui5-table-cell v-if="(obj.ui === 'icon') && (fieldsList.includes('actions'))"
                            class="find-row-cell">
              <ui5-icon name="search" class="table-icon" />
            </ui5-table-cell>
          </template>
        </ui5-table-row>
        <template v-for="(row, id) in recs">
          <ui5-table-row :type="activeRow"
                         @click="activeRowEvent && activeRowEvent(row)">
            <ui5-table-cell style="white-space: nowrap" :class="row.warning && 'warning-row-cell'">
              <p v-if="!(tableBusy)">{{(id+1) + (recCount*(pageNumber-1))}}</p>
            </ui5-table-cell>
            <template v-for="field in tableColumns">
              <template v-if="field.alias !== 'actions'">
                <ui5-table-cell v-if="fieldsList.includes(field.alias)"
                                :class="row.warning && 'warning-row-cell'"
                                :style="'white-space: '+field.whiteSpace">
                  <div v-if="[true, false].includes(row[field.alias])">
                    <div v-if="field.alias === 'sex'">
                      <SexBadge v-bind:sex="row[field.alias]" />
                    </div>
                    <div v-if="field.alias !== 'sex'">
                      <div v-if="row[field.alias].constructor === Array">
                        <template v-for="value in row[field.alias]">
                          <ui5-badge v-if="value.constructor === Object" color-scheme="6">{{value.name}}</ui5-badge>
                          <ui5-badge v-if="value.constructor !== Object" color-scheme="6">{{value}}</ui5-badge>
                        </template>
                      </div>
                      <div v-if="row[field.alias].constructor !== Array">
                        <ui5-badge v-if="row[field.alias] === true"
                                   color-scheme="8">
                          <ui5-icon name="accept" />
                        </ui5-badge>
                        <ui5-badge v-if="row[field.alias] === false"
                                   color-scheme="2">
                          <ui5-icon name="decline" />
                        </ui5-badge>
                      </div>
                    </div>
                  </div>
                  <div v-if="!([true, false].includes(row[field.alias]))">
                    <ui5-checkbox v-if="field.alias === 'checkbox'"
                                  :checked="(checkBoxRecs.includes(row.object_id)) || (checkBoxRecs.includes('all'))"
                                  @change="e => checkBoxRecAction(row.object_id)"/>
                    <template v-if="field.alias !== 'checkbox'">
                      <div v-if="row[field.alias] === null">-</div>
                      <template v-if="row[field.alias] !== null">
                        <div v-if="row[field.alias].constructor === Array">
                          <template v-for="object in row[field.alias]">
                            <ui5-badge  color-scheme="9">
                              {{object}}
                            </ui5-badge><br/><br/>
                          </template>
                        </div>
                        <div v-if="row[field.alias].constructor !== Array">
                          <JournalEventResultBadge v-if="field.alias === 'event_result'"
                                                   v-bind:result="row[field.alias]" />
                          <EventStatus v-if="field.alias === 'event_status'"
                                       v-bind:status="row[field.alias]" />
                          <AppStatus v-if="field.alias === 'app_status'"
                                     v-bind:status="row[field.alias]" />
                          <div v-if="!(['event_result', 'event_status', 'app_status'].includes(field.alias))">
                            {{row[field.alias]}}
                          </div>
                        </div>
                      </template>
                    </template>
                  </div>

                </ui5-table-cell>
              </template>
              <ui5-table-cell v-if="(field.alias === 'actions') && (fieldsList.includes('actions'))"
                              :class="row.warning && 'warning-row-cell'"
                              style="white-space: nowrap">
                <ui5-icon v-if="additionalManageIcon"
                          interactive
                          :class="row.warning && 'additional-row-icon'"
                          :name="additionalManageIcon.icon"
                          @click="additionalManageIcon.function(row.object_id)" />
                &nbsp;&nbsp;
                <ui5-icon interactive
                          :class="row.warning && 'additional-row-icon'"
                          name="edit"
                          @click="editRow = row; action = 'edit'; openAddEditDialog()"/>
                &nbsp;&nbsp;
                <ui5-icon interactive
                          :class="row.warning && 'additional-row-icon'"
                          name="delete"
                          @click="delRec(row.object_id)"/>
              </ui5-table-cell>
            </template>
          </ui5-table-row>
        </template>
      </ui5-table>
    </div>
    <div style="height: 10%">
      <ui5-table :busy="tableBusy" class="no-head-table">
        <ui5-table-row type="Inactive">
          <ui5-table-cell id="pagination_cell" class="find-row-cell" style="width: 100%">
            <div style="display: inline-block">
              Страница:
            </div>&nbsp;
            <div style="display: inline-block">
              <ui5-step-input :value="pageNumber"
                              style="width: 10vw; z-index: 15"
                              :min="1"
                              :max="pageTotal"
                              @change="e => this.pageNumber = e.target.value" />
            </div>&nbsp;
            <div style="display: inline-block;">
              из {{pageTotal}}
            </div>
          </ui5-table-cell>
        </ui5-table-row>
      </ui5-table>
    </div>
  </div>

  <ui5-dialog ref="addEditDialog" class="add-edit-dialog">
    <ui5-bar slot="header">
      <ui5-title v-if="action === 'add'" level="H5" slot="startContent">Добавление записи</ui5-title>
      <ui5-title v-if="action === 'edit'" level="H5" slot="startContent">Изменение записи</ui5-title>
      <ui5-button design="Emphasized" slot="endContent" icon="decline" @click="e => this.$refs.addEditDialog.close(e.current)"></ui5-button>
    </ui5-bar>
    <div style="height: 99%; overflow: auto">
      <template v-for="obj in fieldsArray">
        <template v-if="!(['object_id', 'actions'].includes(obj.field))">
          <ui5-label show-colon :required="obj.add_required && true">{{ tableColumns.filter((col) => col.alias === obj.field)[0].name }}</ui5-label>
          <template v-if="action === 'add'">
            <template v-if="noAddEditField.includes(obj.field)">-</template>
            <template v-if="(obj.ui !== 'icon') && !(noAddEditField.includes(obj.field))">
              <p v-if="['None', 'checkbox'].includes(obj.ui)">-</p>
              <PasswordField ref="add_password" v-if="obj.ui === 'password'" />
              <ui5-input v-if="obj.ui === 'input'"
                         :type="obj.type"
                         :ref="'add_'+obj.field"
                         :value-state="obj.add_required && 'Warning'"
                         :show-suggestions="obj.add_required">
                <div v-if="obj.add_required" slot="valueStateMessage">Обязательно для заполнения</div>
              </ui5-input>
              <ui5-switch v-if="obj.ui === 'switch'" :ref="'add_'+obj.field" />
              <ui5-select v-if="obj.ui === 'select'"
                          :ref="'add_'+obj.field"
                          :value-state="obj.add_required && 'Warning'"
                          :show-suggestions="obj.add_required">
                <template v-for="option in obj.options">
                  <ui5-option  v-if="option.name.length > 0">
                    {{option.name}}
                  </ui5-option>
                </template>
                <div v-if="obj.add_required" slot="valueStateMessage">Обязательно для заполнения</div>
              </ui5-select>
              <ui5-multi-combobox v-if="obj.ui === 'multiple'"
                                  :ref="'add_'+obj.field"
                                  :value-state="obj.add_required && 'Warning'"
                                  :show-suggestions="obj.add_required">\
                <template v-for="option in obj.options">
                  <ui5-mcb-item  v-if="option.name !== ''" :text="option.name" />
                </template>
                <div v-if="obj.add_required" slot="valueStateMessage">Обязательно для заполнения</div>
              </ui5-multi-combobox>
              <ui5-date-picker v-if="obj.ui === 'date_picker'"
                               format-pattern="dd.MM.yyyy"
                               :ref="'add_'+obj.field"
                               :value="componentGetDay(false)"
                               :value-state="obj.add_required && 'Warning'"
                               :show-suggestions="obj.add_required">
                <div v-if="obj.add_required" slot="valueStateMessage">Обязательно для заполнения</div>
              </ui5-date-picker>
              <ui5-datetime-picker v-if="obj.ui === 'datetime_picker'"
                                   format-pattern="dd.MM.yyyy HH:mm"
                                   :ref="'add_'+obj.field"
                                   :value="componentGetDay(false)+' 12:00'"
                                   :value-state="obj.add_required && 'Warning'"
                                   :show-suggestions="obj.add_required">
                <div v-if="obj.add_required" slot="valueStateMessage">Обязательно для заполнения</div>
              </ui5-datetime-picker>
              <ui5-daterange-picker v-if="obj.ui === 'date_range_picker'"
                                    format-pattern="dd.MM.yyyy"
                                    :ref="'add_'+obj.field"
                                    :value="componentGetDay(false)+' - '+componentGetDay(false)"
                                    :value-state="obj.add_required && 'Warning'"
                                    :show-suggestions="obj.add_required">
                <div v-if="obj.add_required" slot="valueStateMessage">Обязательно для заполнения</div>
              </ui5-daterange-picker>
            </template>
          </template>

          <template v-if="action === 'edit'">
            <template v-if="noAddEditField.includes(obj.field)">
              <ui5-select v-if="['CREATED', 'PUBLISHED', 'REMOVED'].includes(editRow[obj.field])"
                          ref="edit_event_status">
                <ui5-option value="PUBLISHED" :selected="editRow[obj.field] === 'PUBLISHED'">Опубликовано</ui5-option>
                <ui5-option value="CANCELED" :selected="editRow[obj.field] === 'CANCELED'">Отменено</ui5-option>
                <ui5-option value="REMOVED" :selected="editRow[obj.field] === 'REMOVED'">Снято с публикации</ui5-option>
              </ui5-select>
              <ui5-select v-if="!(['CREATED', 'PUBLISHED', 'REMOVED'].includes(editRow[obj.field]))"
                          ref="edit_event_status" readonly>
                <ui5-option :value="row[obj.field]">
                  {{getEventStatusDisplayName(editRow[obj.field])}}
                </ui5-option>
              </ui5-select>
            </template>
            <template v-if="(obj.ui !== 'icon') && !(noAddEditField.includes(obj.field))">
              <PasswordField v-if="obj.ui === 'password'"
                             ref="edit_password" />
              <ui5-input v-if="obj.ui === 'input'"
                         :type="obj.type"
                         :ref="'edit_'+obj.field"
                         :value="editRow[obj.field]"
                         :value-state="obj.add_required && 'Warning'"
                         :show-suggestions="obj.add_required">
                <div v-if="obj.add_required" slot="valueStateMessage">Обязательно для заполнения</div>
              </ui5-input>
              <ui5-switch v-if="obj.ui === 'switch'"
                          :ref="'edit_'+obj.field"
                          :checked="editRow[obj.field]" />
              <ui5-select v-if="obj.ui === 'select'"
                          :ref="'edit_'+obj.field"
                          :value-state="obj.add_required && 'Warning'"
                          :show-suggestions="obj.add_required">
                <template v-for="option in obj.options">
                  <ui5-option v-if="option !== ''"
                              :selected="editRow[obj.field] === option.name">
                    {{option.name}}
                  </ui5-option>
                </template>
                <div v-if="obj.add_required" slot="valueStateMessage">Обязательно для заполнения</div>
              </ui5-select>
              <ui5-multi-combobox v-if="obj.ui === 'multiple'"
                                  :ref="'edit_'+obj.field"
                                  :value-state="obj.add_required && 'Warning'"
                                  :show-suggestions="obj.add_required">
                <template v-for="option in obj.options">
                  <ui5-mcb-item v-if="option.name !== ''"
                                :text="option.name"
                                :selected="editRow[obj.field].filter((value) => value === option.name).length > 0"/>
                </template>
                <div v-if="obj.add_required" slot="valueStateMessage">Обязательно для заполнения</div>
              </ui5-multi-combobox>
              <ui5-date-picker v-if="obj.ui === 'date_picker'"
                               format-pattern="dd.MM.yyyy"
                               :ref="'edit_'+obj.field"
                               :value-state="obj.add_required && 'Warning'"
                               :value="editRow[obj.field]"
                               :show-suggestions="obj.add_required">
                <div v-if="obj.add_required" slot="valueStateMessage">Обязательно для заполнения</div>
              </ui5-date-picker>
              <ui5-datetime-picker v-if="obj.ui === 'datetime_picker'"
                                   format-pattern="dd.MM.yyyy HH:mm"
                                   :ref="'edit_'+obj.field"
                                   :value-state="obj.add_required && 'Warning'"
                                   :value="editRow[obj.field]"
                                   :show-suggestions="obj.add_required">
                <div v-if="obj.add_required" slot="valueStateMessage">Обязательно для заполнения</div>
              </ui5-datetime-picker>
              <ui5-daterange-picker v-if="obj.ui === 'date_range_picker'"
                                    format-pattern="dd.MM.yyyy"
                                    :ref="'edit_'+obj.field"
                                    :value="editRow[obj.field]"
                                    :value-state="obj.add_required && 'Warning'"
                                    :show-suggestions="obj.add_required">
                <div v-if="obj.add_required" slot="valueStateMessage">Обязательно для заполнения</div>
              </ui5-daterange-picker>
            </template>
          </template>
        </template>
      </template>
    </div>
    <div slot="footer" style="display: flex; justify-content: flex-end; width: 100%; align-items: center">
      <div style="flex: 1;"></div>
      <div v-if="addEditError.length > 0" >
        <ui5-message-strip design="Negative" hide-close-button>
          {{ addEditError }}
        </ui5-message-strip>
      </div>&nbsp;
      <ui5-button v-if="action === 'add'" design="Emphasized"
                  icon="add" @click="addRec()">Добавить</ui5-button>
      <ui5-button v-if="action === 'edit'" design="Emphasized"
                  icon="edit" @click="editRec()">Изменить</ui5-button>
    </div>
  </ui5-dialog>
</template>

<script>
import PasswordField from "../PasswordField.vue";
import SexBadge from "../badges/SexBadge.vue";
import PhoneField from "../PhoneField.vue";
import JournalEventResultBadge from "../badges/JournalEventResultBadge.vue";
import EventStatus from "../badges/EventStatus.vue";
import {event_status_db_name, event_status_display_name} from "../../additional/functions/event_status_display_name.js";
import {apiRequest} from "../../additional/functions/api_request.js";
import AppStatus from "../badges/AppStatus.vue";
import {
  changeTableView,
  changeTimePickerIconTransform,
  getDay,
  noHeadTable
} from "../../additional/functions/additional.js";
import {showMessage} from "../../additional/functions/message-strips.js";
import ProfileForm from "../ProfileForm.vue";
import {disableDialogLayer} from "../../additional/functions/disableDialogLayer.js";

export default {
  name: 'PaginationTable',
  components: {ProfileForm, AppStatus, EventStatus, JournalEventResultBadge, PhoneField, SexBadge, PasswordField},
  props: {
    tableMode: {type: String},
    outsideFilterString: {type: String},
    recsURL: {type: String},
    recAddURL: {type: String},
    recEditURL: {type: String},
    recDeleteURL: {type: String},
    info: {type: Boolean},
    infoText: {type: String},
    searchRow: {type: Boolean},
    changeShowFields: {type: Boolean},
    colCount: {type: Number},
    activeRow: {type: String},
    activeRowEvent: {type: Function},
    addButton: {type: Boolean},
    tableColumns: {type: Array},
    fieldsArray: {type: Array},
    dataTableHeight: {type: Number},
    additionalManageIcon: {type: Object},
  },
  data() {
    return {
      checkInit: true,
      noAddEditField: ['event_status',],
      filterString: this.outsideFilterString || '',
      recs: [],
      states: [],
      additionalData: {},
      tableBusy: true,
      fieldsList: [],
      recsTotalCount: 0,
      pageNumber: 1,
      pageTotal: 1,
      checkBoxRecs: [],
      recCount: this.$store.state.recCountOptions.split(',')[0],
      recCountOptions: this.$store.state.recCountOptions.split(','),
      action: 'add',
      addEditError: '',
      editRow: {},
      editPasswordValue: ''
    }
  },
  methods: {
    openAddEditDialog() {
      this.$refs.addEditDialog.show()
      setTimeout(disableDialogLayer, 25)
      setTimeout(changeTimePickerIconTransform, 25)
    },
    init() {
      this.setDefaultListFields()
      setTimeout(() => {
        changeTableView()
        noHeadTable()
        try {
          document.querySelector('#pagination_cell').shadowRoot.querySelector('td').colSpan = this.colCount
        } catch (e) {}
        this.getRecs(0, this.recCount)
      }, 25)
    },
    setDefaultListFields() {
      this.tableColumns.map((column) => {
          if (column.alias !== 'object_id') {
            this.fieldsList.push(column.alias)
          }
      })
    },
    componentGetDay(yesterday) {
      return getDay(yesterday)
    },
    changeFieldView(items) {
      this.fieldsList = []
      if (items.length === 0) {
        return false
      }
      items.map((field) => {
        this.fieldsList.push(this.tableColumns.filter((column) => column.name === field._state.text)[0].alias)
      })
      setTimeout(changeTableView, 25)
    },
    checkBoxRecAction(value) {
      if (value === 'all') {
        if (!(this.$refs.mainCheckBox[0]._state.checked)) {
          this.checkBoxRecs = []
        } else if ((this.checkBoxRecs.length === this.recs) && (this.$refs.mainCheckBox[0]._state.checked)) {
          return true
        } else if ((this.checkBoxRecs.length !== this.recs) && (this.$refs.mainCheckBox[0]._state.checked)) {
          this.recs.map((row) => {
            if (!(this.checkBoxRecs.includes(row.object_id))) {
              this.checkBoxRecs.push(row.object_id)
            }
          })
        } else {}
      } else {
        if (this.checkBoxRecs.includes(value)) {
          let index = this.checkBoxRecs.indexOf(value)
          this.checkBoxRecs.splice(index, 1)
        } else {
          this.checkBoxRecs.push(value)
        }
      }
    },
    async getRecs(start, size) {
      if (this.checkInit) {
        if (this.outsideFilterString) {
          let initFilterArr = this.outsideFilterString.split('&')
          initFilterArr.map((rec) => {
            if (rec.length > 0) {
              let recArr = rec.split('=')
              this.$refs['filter_'+recArr[0]][0].value=recArr[1]
            }
          })
        }
        this.checkInit = false
      }
      let url = this.recsURL+'?size='+size+'&start='+start
      if (this.filterString.length > 0) {
        url += this.filterString
      }
      apiRequest(
          url,
          'GET',
          true,
          null,
          false,
          false
      )
          .then(data => {
            if (data.error) {
              showMessage('error', data.error, false)
              this.recs=[]
            } else {
              this.recs = data.results
              this.recsTotalCount = data.count
              this.pageTotal = Math.ceil(this.recsTotalCount/this.recCount)
            }
            this.tableBusy = false

          })
    },
    filterPhone() {
      this.filterRecs(this.$refs.filter_phone[0].componentPhoneField, 'phone')
    },
    filterRecs(value, field) {
      let filters = this.filterString
      if (this.filterString.length > 0) {
        let filterArr = this.filterString.substring(1).split('&')
        let index = -1
        for (let i=0;i<filterArr.length;i++) {
          if (filterArr[i].split('=')[0] === field) {
            index = i
            break;
          }
        }
        if (index !== -1) {
          filterArr.splice(index, 1)
          if (filterArr.length > 0) {
            let filter_str = '&'
            filterArr.map((el) => {
              filter_str += el+' &'
            })
            filters = filter_str.slice(0, -1)
          } else {
            filters = ''
          }
        }
      }
      if (value !== '') {
        filters = filters+'&'+field+'='+value
      }
      this.filterString = filters
    },
    async addRec() {
      let data = {}
      let value = null
      let add_required = false
      this.fieldsArray.map((column) => {
        if (!(['object_id', 'actions'].includes(column.field))) {
          switch(column.ui) {
            case 'input':
            case 'date_picker':
            case 'datetime_picker':
            case 'date_range_picker':
              try {
                value = this.$refs['add_'+column.field][0].value
              } catch (e) {
                if (column.add_required) {
                  add_required = true
                  return false
                }
              }
              break

            case 'select':
              if (column.field === 'event_status') {
                value = 'CREATED'
              } else {
                try {
                  value = this.$refs['add_'+column.field][0].selectedOption.innerText
                } catch (e) {
                  if (column.add_required) {
                    add_required = true
                    return false
                  }
                }
              }
              break

            case 'multiple':
              try {
                value = []
                this.$refs['add_'+column.field][0].selectedValues.map((select_value) => {
                  value.push(column.options.filter((option) => option.name === select_value._state.text)[0].name)
                })
              } catch (e) {
                if (column.add_required) {
                  add_required = true
                  return false
                }
              }
              break

            case 'password':
              try {
                value = this.$refs.add_password.value
              } catch (e) {
                if (column.add_required) {
                  add_required = true
                  return false
                }
              }
          }
          if ((value.length === 0) && (column.add_required)) {
            add_required = true
            return false
          }
          data[column.field] = value
        }
      })
      if (add_required) {
        showMessage('error', 'Заполните обязательные поля формы')
        return false
      }
      this.tableBusy = true
      apiRequest(
          this.recAddURL,
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
                this.getRecs((this.pageNumber-1)*this.recCount, this.recCount)
                this.$refs.addEditDialog.close()
              }
              this.tableBusy = false
            })
    },
    async editRec() {
      let data = {}
      let value = null
      let add_required = false
      this.fieldsArray.map((column) => {
        if (column.field === 'event_status') {
          data['event_status'] = event_status_db_name(this.$refs.edit_event_status[0].selectedOption.innerText)
        } else {
          if (!(['object_id', 'actions'].includes(column.field))) {
            switch(column.ui) {
              case 'input':
              case 'date_picker':
              case 'datetime_picker':
              case 'date_range_picker':
                try {
                  value = this.$refs['edit_'+column.field][0].value
                } catch (e) {
                  if (column.add_required) {
                    add_required = true
                    return false
                  }
                }

                break

              case 'select':
                try {
                  value = this.$refs['edit_'+column.field][0].selectedOption.innerText
                } catch (e) {
                  if (column.add_required) {
                    add_required = true
                    return false
                  }
                }
                break

              case 'multiple':
                try {
                  value = []
                  this.$refs['edit_'+column.field][0].selectedValues.map((select_value) => {
                    value.push(column.options.filter((option) => option.name === select_value._state.text)[0].name)
                  })
                } catch (e) {
                  if (column.add_required) {
                    add_required = true
                    return false
                  }
                }
                break

              case 'password':
                try {
                  value = this.$refs.edit_password.value
                } catch (e) {
                  if (column.add_required) {
                    add_required = true
                    return false
                  }
                }
            }
            if ((value.length === 0) && (column.add_required)) {
              add_required = true
              return false
            }
            data[column.field] = value
          }
        }
      })
      if (add_required) {
        showMessage('error', 'Заполните обязательные поля формы')
        return false
      }
      this.tableBusy = true
      apiRequest(
          this.recEditURL+this.editRow.object_id+'/',
          'PATCH',
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
              this.getRecs((this.pageNumber-1)*this.recCount, this.recCount)
              this.$refs.addEditDialog.close()
            }
            this.tableBusy = false
          })
    },
    async delRec(object_id) {
      if (confirm('Вы уверены, что хотите выполнить удаление?')) {
        this.tableBusy = true
        apiRequest(
            this.recDeleteURL+object_id+'/',
            'DELETE',
            true,
            null,
            false,
            false
        )
            .then(data => {
              if (data['error']) {
                showMessage('error', data['error'])
              } else {
                showMessage('success', data['success'])
                this.getRecs((this.pageNumber-1)*this.recCount, this.recCount)
              }
              this.tableBusy = false
            })
      }
    },
    getEventStatusDisplayName(event_status) {
      return event_status_display_name(event_status)
    }
  },
  watch: {
    pageNumber: function() {
      if (this.pageNumber !== 0) {
        this.tableBusy = true
        this.getRecs((this.pageNumber-1)*this.recCount, this.recCount)
      }
    },
    fieldsList: function() {
      changeTableView()
    },
    recCount: function() {
      this.pageTotal = Math.ceil(this.recsTotalCount/this.recCount)
      if (this.pageNumber === 1) {
        this.tableBusy = true
        this.getRecs((this.pageNumber-1)*this.recCount, this.recCount)
      } else {
        this.pageNumber = 1
      }
    },
    filterString: function() {
      this.pageTotal = Math.ceil(this.recsTotalCount/this.recCount)
      if (this.pageNumber === 1) {
        this.tableBusy = true
        this.getRecs((this.pageNumber-1)*this.recCount, this.recCount)
      } else {
        this.pageNumber = 1
      }
    },
  },
  mounted() {
    this.$nextTick(function () {
      this.init()
    })
  }
}
</script>

<style>

#data_table {
  width: 100%;
  overflow: auto
}

.upper-table-container {
  display: flex;
  justify-content: space-between;
}

.find-row-cell {
  background-color: #dddde2;
}

.additional-row-cell {
  background-color: #00455d;
  color: white;
}

.warning-row-cell {
  background-color: #e55c02;
  color: white;
}

.additional-row-icon {
  color: white;
}
</style>