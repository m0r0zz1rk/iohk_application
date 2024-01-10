<template>
  <div style="margin-left: 4px;">
    <div style="height: 10%">
      <div>
        <div class="upper-table-container">
          <div>
            <div v-if="addButton && canChange" style="display: inline-block">
              <ui5-button icon="add"
                          @click="addRow = true">Добавить</ui5-button>
              &nbsp;
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
        </div>
      </div>
    </div><br/>
    <div>
      <ui5-table :style="tableCss"
                 :busy="tableBusy"
                 mode="None"
                 sticky-column-header>
        <ui5-table-column slot="columns">№</ui5-table-column>
        <ui5-table-column v-for="col in partAppFields"
                          style="white-space: nowrap; width: 15vw;"
                          slot="columns">
          {{col.name}}
        </ui5-table-column>
        <ui5-table-column v-if="canChange"
                          style="white-space: nowrap"
                          slot="columns">Действия</ui5-table-column>
        <ui5-table-row v-if="addRow && canChange">
          <ui5-table-cell class="additional-row-cell">
            <ui5-icon name="add" style="color: white" />
          </ui5-table-cell>
          <ui5-table-cell v-for="field in partAppFields"
                          class="additional-row-cell">
              <div v-if="InputTypes.includes(field.type)">
                <ui5-input v-if="field.type.includes('profile_')"
                           :ref="'add_'+field.object_id"
                           :value="getProfileInfoByField(field.type)"
                           readonly />
                <ui5-input v-if="!(field.type.includes('profile_'))"
                           :ref="'add_'+field.object_id"
                           :type="field.type.charAt(0).toUpperCase()+field.type.slice(1)" />
              </div>
              <ui5-date-picker v-if="field.type === 'date'"
                               formatPattern="dd.MM.YYYY"
                               :ref="'add_'+field.object_id" />
              <ui5-daterange-picker v-if="field.type === 'date_range'"
                                    formatPattern="dd.MM.YYYY"
                                    :ref="'add_'+field.object_id"
                                    :value = "field.value" />
              <ui5-select v-if="field.type === 'select'"
                          :ref="'add_'+field.object_id">
                <ui5-option selected></ui5-option>
                <ui5-option v-for="option in field.available_values">{{option}}</ui5-option>
              </ui5-select>
              <ui5-multi-combobox v-if="field.type === 'multiple'"
                                  :ref="'add_'+field.object_id">
                <ui5-mcb-item v-for="option in field.available_values"
                              :text="option" />
              </ui5-multi-combobox>
              <PhoneField v-if="field.type === 'phone'"
                          :ref="'add_'+field.object_id" />
          </ui5-table-cell>
          <ui5-table-cell class="additional-row-cell">
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
        </ui5-table-row>
        <template v-for="rec in recs">
          <ui5-table-row v-if="editRow !== rec.rec_id">
            <ui5-table-cell style="white-space: nowrap; width: 50px;">{{rec.rec_id}}</ui5-table-cell>
            <ui5-table-cell v-for="field in partAppFields">
              {{rec.fields.filter((rec_field) => rec_field.field_id===field.object_id)[0].value}}
            </ui5-table-cell>
            <ui5-table-cell v-if="canChange"
                            style="white-space: nowrap; width: 150px;">
              <ui5-icon interactive
                        name="edit"
                        @click="editRow = rec.rec_id"/>
              &nbsp;&nbsp;
              <ui5-icon interactive
                        name="delete"
                        @click="delRec(rec.rec_id)"/>
            </ui5-table-cell>
          </ui5-table-row>
          <ui5-table-row v-if="(editRow === rec.rec_id) && canChange">
            <ui5-table-cell class="additional-row-cell">
              <ui5-icon name="edit" style="color: white"/>
            </ui5-table-cell>
            <ui5-table-cell v-for="field in partAppFields"
                            class="additional-row-cell">
              <div v-if="InputTypes.includes(field.type)">
                <ui5-input v-if="field.type.includes('profile_')"
                           :ref="'edit_'+field.object_id"
                           :value="getProfileInfoByField(field.type)"
                           readonly />
                <ui5-input v-if="!(field.type.includes('profile_'))"
                           :ref="'edit_'+field.object_id"
                           :type="field.type.charAt(0).toUpperCase()+field.type.slice(1)"
                           :value="rec.fields.filter((rec_field) => rec_field.field_id===field.object_id)[0].value" />
              </div>
              <ui5-date-picker v-if="field.type === 'date'"
                               formatPattern="dd.MM.YYYY"
                               :ref="'edit_'+field.object_id"
                               :value="rec.fields.filter((rec_field) => rec_field.field_id===field.object_id)[0].value" />
              <ui5-daterange-picker v-if="field.type === 'date_range'"
                                    formatPattern="dd.MM.YYYY"
                                    :ref="'edit_'+field.object_id"
                                    :value = "rec.fields.filter((rec_field) => rec_field.field_id===field.object_id)[0].value" />
              <ui5-select v-if="field.type === 'select'"
                          :ref="'edit_'+field.object_id">
                <ui5-option v-for="option in field.available_values"
                            :selected="rec.fields.filter(
                                (rec_field) => rec_field.field_id===field.object_id
                                )[0].value === option">{{option}}</ui5-option>
              </ui5-select>
              <ui5-multi-combobox v-if="field.type === 'multiple'"
                                  :ref="'edit_'+field.object_id">
                <ui5-mcb-item v-for="option in field.available_values"
                              :text="option"
                              :selected="rec.fields.filter(
                                  (rec_field) => rec_field.field_id===field.object_id
                                  )[0].value.split(',').includes(option)"/>
              </ui5-multi-combobox>
              <PhoneField v-if="field.type === 'phone'"
                          v-bind:phone-value="rec.fields.filter(
                              (rec_field) => rec_field.field_id===field.object_id
                              )[0].value"
                          :ref="'edit_'+field.object_id"
              />
            </ui5-table-cell>
            <ui5-table-cell style="white-space: nowrap"
                            class="additional-row-cell">
              <div>
                <ui5-icon interactive
                          class="additional-row-icon"
                          name="accept"
                          @click="editRec(rec.rec_id)"/>
                &nbsp;&nbsp;
                <ui5-icon interactive
                          class="additional-row-icon"
                          name="decline"
                          @click="editRow = 0" />
              </div>
            </ui5-table-cell>
          </ui5-table-row>
        </template>
      </ui5-table>
    </div>
  </div>
</template>

<script>

import PhoneField from "../PhoneField.vue";
import InputFormFieldTypes from "../../additional/consts/html_app_form_field_types.js";
import {apiRequest} from "../../additional/functions/api_request.js";

export default {
  name: 'PartAppsTable',
  components: {PhoneField},
  props: {
    canChange: {type: Boolean},
    eventId: {type: String},
    recsURL: {type: String},
    recAddURL: {type: String},
    recEditURL: {type: String},
    recDeleteURL: {type: String},
    partAppFields: {type: Array},
    addButton: {type: Boolean},
    info: {type: Boolean},
    dataTableHeight: {type: Number},
  },
  data() {
    return {
      InputTypes: InputFormFieldTypes,
      filterString: '',
      recs: [],
      addRow: false,
      editRow: 0,
      tableBusy: true,
      profileData: {}
    }
  },
  methods: {
    async getRecs() {
      let url = this.$store.state.backendUrl+this.recsURL
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
              this.recs = data
            }
            this.tableBusy = false
          })
    },
    async getProfileInfo() {
      apiRequest(
          this.$store.state.backendUrl+'/api/v1/auth/profile/',
          'GET',
          true,
          null,
          false,
          false
      )
          .then(data => {
            if (data.error) {
              showMessage('error', data.error, false)
            } else {
              this.profileData = data
            }
          })
    },
    getProfileInfoByField(field) {
      if (field !== 'profile_fio') {
        let arr = field.split('_')
        let prof_info = ''
        if (arr.length === 3) {
          prof_info = arr[1]+'_'+arr[2]
        } else {
          prof_info = arr[1]
        }
        if (Object.keys(this.profileData).includes(prof_info)) {
          return this.profileData[prof_info]
        }
      }
      let fio = ''
      if ((Object.keys(this.profileData).includes('surname')) &&
          (Object.keys(this.profileData).includes('name'))) {
        fio = this.profileData.surname+' '+this.profileData.name
      }
      if ((Object.keys(this.profileData).includes('patronymic'))) {
        fio += ' '+this.profileData.patronymic
      }
      return fio
    },
    async addRec() {
      if (!(this.canChange)) {return false}
      let data = {
        rec_id: this.recs.length + 1
      }
      let value = null
      let blank = false
      let fields = []
      this.partAppFields.map((field) => {
        if (['date', 'date_range', ...this.InputTypes].includes(field.type)) {
          value = this.$refs['add_' + field.object_id][0].value
        } else if (field.type === 'select') {
          value = this.$refs['add_' + field.object_id][0].selectedOption.innerText
        } else if (field.type === 'multiple') {
          value = ''
          this.$refs['add_' + field.object_id][0].selectedValues.map((val) => {
            value += val._state.text + ','
          })
          value = value.slice(0, -1)
        } else if (field.type === 'phone') {
          value = this.$refs['add_' + field.object_id][0].componentPhoneField
        } else {
        }
        if (value.length === 0) {
          blank=true
        }
        field = {
          field_id: field.object_id,
          value: value
        }
        fields.push(field)
      })
      if (blank) {
        showMessage('error', 'Заполните все поля заявки')
        return false
      }
      data['fields'] = fields
      console.log(data)
      this.tableBusy = true
      apiRequest(
          this.$store.state.backendUrl+this.recAddURL,
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
              this.getRecs()
            }
            this.tableBusy = false
          })
    },
    async editRec(rec_id) {
      if (!(this.canChange)) {return false}
      let data = {
        rec_id: rec_id
      }
      let value = null
      let blank = false
      let fields = []
      this.partAppFields.map((field) => {
        if (['date', 'date_range', ...this.InputTypes].includes(field.type)) {
          value = this.$refs['edit_' + field.object_id][0].value
        } else if (field.type === 'select') {
          value = this.$refs['edit_' + field.object_id][0].selectedOption.innerText
        } else if (field.type === 'multiple') {
          value = ''
          this.$refs['edit_' + field.object_id][0].selectedValues.map((val) => {
            value += val._state.text + ','
          })
          value = value.slice(0, -1)
        } else if (field.type === 'phone') {
          value = this.$refs['edit_' + field.object_id][0].componentPhoneField
        } else {
        }
        if (value.length === 0) {
          blank=true
        }
        field = {
          field_id: field.object_id,
          value: value
        }
        fields.push(field)
      })
      if (blank) {
        showMessage('error', 'Заполните все поля заявки')
        return false
      }
      data['fields'] = fields
      this.tableBusy = true
      apiRequest(
          this.$store.state.backendUrl+this.recEditURL,
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
              this.getRecs()
            }
            this.tableBusy = false
          })
    },
    async delRec(rec_id) {
      if (!(this.canChange)) {return false}
      if (confirm('Вы уверены, что хотите удалить заявку?')) {
        this.tableBusy = true
        apiRequest(
            this.$store.state.backendUrl+'/api/v1/users/app_form_fields/part_app_delete/',
            'DELETE',
            true,
            {
              event_id: this.eventId,
              rec_id: rec_id
            },
            false,
            false
        )
            .then(data => {
              if (data['error']) {
                showMessage('error', data['error'])
              } else {
                showMessage('success', data['success'])
                this.getRecs()
              }
              this.tableBusy = false
            })
      }
    }
  },
  mounted() {
    setTimeout(() => {
      changeTableView()
      noHeadTable()
      try {
        document.querySelector('#pagination_cell').shadowRoot.querySelector('td').colSpan = this.colCount
      } catch (e) {

      }
      this.getRecs()
      this.getProfileInfo()
    }, 25)
  },
  computed: {
    tableCss() {
      return {
        width: `calc(20vw*${this.partAppFields.length})`,
        height: `height: ${this.dataTableHeight}vh`,
        overflow: `auto`
      };
    },
    dataTable() {
      return {
        width: `100%`,
        height: `height: ${this.dataTableHeight}vh`
      }
    }
  },
  watch: {
    canChange() {
      setTimeout(() => {
        changeTableView()
        noHeadTable()
      }, 25)
    }
  }
}

</script>

<style scoped>
.data_table {
  width: 100%;
}
</style>