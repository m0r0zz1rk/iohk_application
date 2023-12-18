<template>
  <div style="margin-left: 4px;">
    <div style="height: 10%">
      <div>
        <div class="upper-table-container">
          <div>
            <ui5-button v-if="this.addButton"
                        icon="add"
                        @click="addRow = true">Добавить</ui5-button>
            &nbsp;
            <ui5-button v-if="this.changeShowFields"
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
            <ui5-button v-if="this.info"
                        icon="information"
                        @click="this.$refs.info_popover.showAt($event.detail.targetRef)">
              Справка
            </ui5-button>
            <ui5-popover v-if="this.info"
                         placement-type="Right">
              {{infoText}}
            </ui5-popover>
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
              <ui5-checkbox refs="mainCheckBox"
                            @change="checkBoxRecAction('all')" />
            </div>
            <div v-if="col.name !== 'checkbox'">
              {{col.name}}
            </div>
          </ui5-table-column>
        </template>
        <ui5-table-row v-if="searchRow">
          <ui5-table-cell class="find-row-cell">
            <ui5-icon name="search" />
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
                             :type="obj.type"
                             @change="e => filterRecs(e.target.value, obj.field)" />
                </template>
                <template v-if="obj.ui === 'switch'">
                  <div>
                    <div style="display: inline-block">
                      <ui5-switch :text-on="obj.field === 'sex' && 'М'"
                                  :text-off="obj.field === 'sex' && 'Ж'"
                                  @change="e => filterRecs(e.target._state.checked, obj.field)"/>
                    </div>
                    <div style="display: inline-block">
                      <ui5-icon interactive
                                name="clear-filter"
                                @click="e => filterRecs('', obj.field)" />
                    </div>
                  </div>
                </template>
                <ui5-select v-if="['select', 'multiple'].includes(obj.ui)"
                            @change="e => filterRecs(e.detail.selectedOption.innerText, obj.field)">
                  <ui5-option v-for="option in obj.options">
                    {{option.name}}
                  </ui5-option>
                </ui5-select>
                <ui5-date-picker v-if="obj.ui === 'date_picker'"
                                 format-pattern="dd.MM.yyyy"
                                 @change="e => filterRecs(e.target.value, obj.field)" />
                <ui5-datetime-picker v-if="obj.ui === 'datetime_picker'"
                                     format-pattern="dd.MM.yyyy HH:mm"
                                     @change="e => filterRecs(e.target.value, obj.field)" />
                <ui5-daterange-picker v-if="obj.ui === 'date_range_picker'"
                                      format-pattern="dd.MM.yyyy"
                                      @change="e => filterRecs(e.target.value, obj.field)"/>
              </ui5-table-cell>
            </template>
            <ui5-table-cell v-if="(obj.ui === 'icon') && (fieldsList.includes('actions'))"
                            class="find-row-cell">
              <ui5-icon name="search" />
            </ui5-table-cell>
          </template>
        </ui5-table-row>
        <ui5-table-row v-if="addRow">
          <ui5-table-cell class="additional-row-cell">
            <ui5-icon name="add" style="color: white" />
          </ui5-table-cell>
          <template v-for="obj in fieldsArray">
            <template v-if="obj.ui !== 'icon'">
              <ui5-table-cell v-if="fieldsList.includes(obj.field)"
                              class="additional-row-cell">
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
              </ui5-table-cell>
            </template>
            <ui5-table-cell v-if="(obj.ui === 'icon') && (fieldsList.includes('actions'))"
                            class="additional-row-cell">
              <div>
                <ui5-icon interactive
                          class="additional-row-icon"
                          name="accept"
                          @click="addRec()" />
                &nbsp;&nbsp;
                <ui5-icon interactive
                          class="additional-row-icon"
                          name="decline"
                          @click="addRow = false" />
              </div>
            </ui5-table-cell>
          </template>
        </ui5-table-row>
        <template v-for="(row, id) in recs">
          <ui5-table-row v-if="editRow !== row.object_id"
                         :type="activeRow"
                         @click="activeRowEvent && activeRowEvent(row)">
            <ui5-table-cell style="white-space: nowrap">
              <p v-if="!(tableBusy)">{{(id+1) + (recCount*(pageNumber-1))}}</p>
            </ui5-table-cell>
            <template v-for="field in tableColumns">
              <template v-if="field.alias !== 'actions'">
                <ui5-table-cell v-if="fieldsList.includes(field.alias)"
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
                                  :checked="checkBoxRecs.includes(row.object_id)"
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
                          <div v-if="field.alias !== 'event_result'">
                            {{row[field.alias]}}
                          </div>
                        </div>
                      </template>
                    </template>
                  </div>

                </ui5-table-cell>
              </template>
              <ui5-table-cell v-if="(field.alias === 'actions') && (fieldsList.includes('actions'))"
                              :style="'white-space: '+field.whiteSpace">
                <ui5-icon interactive
                          name="edit"
                          @click="setEditRow(row)"/>
                &nbsp;&nbsp;
                <ui5-icon interactive
                          name="delete"
                          @click="delRec(row.object_id)"/>
              </ui5-table-cell>
            </template>
          </ui5-table-row>
          <ui5-table-row v-if="editRow === row.object_id"
                         :navigated="activeRow">
            <ui5-table-cell class="additional-row-cell">
              <ui5-icon name="edit" style="color: white"/>
            </ui5-table-cell>
            <template v-for="obj in fieldsArray">
              <template v-if="obj.ui !== 'icon'">
                <ui5-table-cell v-if="fieldsList.includes(obj.field)"
                                class="additional-row-cell">
                  <PasswordField v-if="obj.ui === 'password'"
                                 ref="edit_password" />
                  <ui5-input v-if="obj.ui === 'input'"
                             :type="obj.type"
                             :ref="'edit_'+obj.field"
                             :value="row[obj.field]"
                             :value-state="obj.add_required && 'Warning'"
                             :show-suggestions="obj.add_required">
                    <div v-if="obj.add_required" slot="valueStateMessage">Обязательно для заполнения</div>
                  </ui5-input>
                  <ui5-switch v-if="obj.ui === 'switch'"
                              :ref="'edit_'+obj.field"
                              :checked="row[obj.field]" />
                  <ui5-select v-if="obj.ui === 'select'"
                              :ref="'edit_'+obj.field"
                              :value-state="obj.add_required && 'Warning'"
                              :show-suggestions="obj.add_required">
                    <template v-for="option in obj.options">
                      <ui5-option v-if="option !== ''"
                                  :selected="row[obj.field] === option.name">
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
                                    :selected="row[obj.field].filter((value) => value === option.name).length > 0"/>
                    </template>
                    <div v-if="obj.add_required" slot="valueStateMessage">Обязательно для заполнения</div>
                  </ui5-multi-combobox>
                  <ui5-date-picker v-if="obj.ui === 'date_picker'"
                                   format-pattern="dd.MM.yyyy"
                                   :ref="'edit_'+obj.field"
                                   :value-state="obj.add_required && 'Warning'"
                                   :value="row[obj.field]"
                                   :show-suggestions="obj.add_required">
                    <div v-if="obj.add_required" slot="valueStateMessage">Обязательно для заполнения</div>
                  </ui5-date-picker>
                  <ui5-datetime-picker v-if="obj.ui === 'datetime_picker'"
                                       format-pattern="dd.MM.yyyy HH:mm"
                                       :ref="'edit_'+obj.field"
                                       :value-state="obj.add_required && 'Warning'"
                                       :value="row[obj.field]"
                                       :show-suggestions="obj.add_required">
                    <div v-if="obj.add_required" slot="valueStateMessage">Обязательно для заполнения</div>
                  </ui5-datetime-picker>
                  <ui5-daterange-picker v-if="obj.ui === 'date_range_picker'"
                                        format-pattern="dd.MM.yyyy"
                                        :ref="'edit_'+obj.field"
                                        :value="row[obj.field]"
                                        :value-state="obj.add_required && 'Warning'"
                                        :show-suggestions="obj.add_required">
                    <div v-if="obj.add_required" slot="valueStateMessage">Обязательно для заполнения</div>
                  </ui5-daterange-picker>
                </ui5-table-cell>
              </template>
              <ui5-table-cell v-if="(obj.ui === 'icon') && (fieldsList.includes('actions'))"
                              style="white-space: nowrap"
                              class="additional-row-cell">
                <div>
                  <ui5-icon interactive
                            class="additional-row-icon"
                            name="accept"
                            @click="editRec()"/>
                  &nbsp;&nbsp;
                  <ui5-icon interactive
                            class="additional-row-icon"
                            name="decline"
                            @click="editRow = -1" />
                </div>
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

</template>

<script>
import PasswordField from "./PasswordField.vue";
import SexBadge from "./badges/SexBadge.vue";
import PhoneField from "./PhoneField.vue";
import JournalEventResultBadge from "./badges/JournalEventResultBadge.vue";

export default {
  name: 'PaginationTable',
  components: {JournalEventResultBadge, PhoneField, SexBadge, PasswordField},
  props: {
    tableMode: {type: String},
    recsURL: {type: String},
    recAddURL: {type: String},
    recEditURL: {type: String},
    recDeleteURL: {type: String},
    searchRow: {type: Boolean},
    changeShowFields: {type: Boolean},
    colCount: {type: Number},
    activeRow: {type: String},
    activeRowEvent: {type: Function},
    addButton: {type: Boolean},
    tableColumns: {type: Array},
    fieldsArray: {type: Array},
    dataTableHeight: {type: Number},
  },
  data() {
    return {
      recs: [],
      states: [],
      filterString: '',
      additionalData: {},
      tableBusy: true,
      fieldsList: [],
      info: false,
      infoText: '',
      recsTotalCount: 0,
      pageNumber: 1,
      pageTotal: 1,
      checkBoxRecs: [],
      recCount: this.$store.state.recCountOptions.split(',')[0],
      recCountOptions: this.$store.state.recCountOptions.split(','),
      addRow: false,
      editRow: -1,
      editPasswordValue: ''
    }
  },
  methods: {
    init() {
      this.setDefaultListFields()
      setTimeout(() => {
        changeTableView()
        noHeadTable()
        try {
          document.querySelector('#pagination_cell').shadowRoot.querySelector('td').colSpan = this.colCount
        } catch (e) {

        }

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

    },
    async getRecs(start, size) {
      let url = this.$store.state.backendUrl+this.recsURL+'?size='+size+'&start='+start
      if (this.filterString.length > 0) {
        url += this.filterString
      }
      await fetch(url, {
        method: 'GET',
        headers: {
          'X-CSRFToken': getCookie("csrftoken"),
          'Authorization': 'Token '+getCookie('iohk_token')
        }
      })
          .then(resp => {
            if (resp.status === 200) {
              return resp.json()
            } else {
              if (resp.status === 401) {
                showMessage('error', 'Пожалуйста, войдите в систему', false)
                this.$router.push('/?nextUrl='+window.location.href.split('/')[3])
                return false
              }
              this.recs = []
              this.tableBusy = false
            }
          })
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
              try {
                value = this.$refs['add_'+column.field][0].selectedOption.innerText
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
      await fetch(this.$store.state.backendUrl+this.recAddURL, {
        method: 'POST',
        headers: {
          'X-CSRFToken': getCookie("csrftoken"),
          'Content-Type': 'web_app/json',
          'Authorization': 'Token '+getCookie('iohk_token')
        },
        body: JSON.stringify(data)
      })
          .then(resp => {
            if (resp.status === 401) {
              showMessage('error', 'Пожалуйста, войдите в систему', false)
              this.$router.push('/?nextUrl='+window.location.href.split('/')[3])
              return false
            } else {
              return resp.json()
            }
          })
          .then(data => {
            if (data['error']) {
              showMessage('error', data['error'])
            } else {
              showMessage('success', data['success'])
              this.getRecs((this.pageNumber-1)*this.recCount, this.recCount)
            }
            this.tableBusy = false
          })
    },
    async editRec() {
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
      })
      if (add_required) {
        showMessage('error', 'Заполните обязательные поля формы')
        return false
      }
      this.tableBusy = true
      let obj_id = this.editRow
      await fetch(this.$store.state.backendUrl+this.recEditURL+obj_id+'/', {
        method: 'PATCH',
        headers: {
          'X-CSRFToken': getCookie("csrftoken"),
          'Content-Type': 'web_app/json',
          'Authorization': 'Token '+getCookie('iohk_token')
        },
        body: JSON.stringify(data)
      })
          .then(resp => {
            if (resp.status === 401) {
              showMessage('error', 'Пожалуйста, войдите в систему', false)
              this.$router.push('/?nextUrl='+window.location.href.split('/')[3])
              return false
            } else {
              return resp.json()
            }
          })
          .then(data => {
            if (data['error']) {
              showMessage('error', data['error'])
            } else {
              showMessage('success', data['success'])
              this.getRecs((this.pageNumber-1)*this.recCount, this.recCount)

            }
            this.tableBusy = false
          })
    },
    async delRec(object_id) {
      if (confirm('Вы уверены, что хотите выполнить удаление?')) {
        this.tableBusy = true
        await fetch(this.$store.state.backendUrl+this.recDeleteURL+object_id+'/', {
          method: 'DELETE',
          headers: {
            'X-CSRFToken': getCookie("csrftoken"),
            'Content-Type': 'web_app/json',
            'Authorization': 'Token '+getCookie('iohk_token')
          },
        })
            .then(resp => {
              if (resp.status === 200) {
                return resp.json()
              } else {
                if (resp.status === 401) {
                  showMessage('error', 'Пожалуйста, войдите в систему', false)
                  this.$router.push('/?nextUrl='+window.location.href.split('/')[3])
                  return false
                }
                showMessage('error', 'Произошла ошибка, повторите попытку позже')
                this.tableBusy = false
              }
            })
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
    setEditRow(row) {
      this.editRow = row.object_id
      if (this.tableColumns.filter((field) => field.alias === 'password').length > 0) {
        this.$refs.edit_password.passwordStr = row.password
      }
    },
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
    this.init()
  }
}
</script>

<style scoped>

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

.additional-row-icon {
  color: white;
}
</style>