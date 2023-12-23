<template>
  <LkBase ref="baseComponent">
    <slot>
      <ui5-card class="full-card">
        <ui5-card-header slot="header"
                         title-text="Управление мероприятием">
        </ui5-card-header>
        <div style="width: 100%; text-align: center; justify-content: center">
          <div style="display: inline-block">
            <table>
              <tr>
                <td>Мероприятие:</td>
                <td>
                  <div v-if="selectedEvent === null">
                    <ui5-badge color-scheme="3">Не выбрано</ui5-badge>
                  </div>
                  <div v-if="selectedEvent !== null">
                    <b>{{selectedEvent.name}} ({{selectedEvent.date_range}})</b>
                  </div>
                </td>
              </tr>
              <tr>
                <td colspan="2">
                  <ui5-button icon="search"
                              @click="e => $refs.findEventDialog.show(e.target)">
                    Поиск мероприятия
                  </ui5-button>
                </td>
              </tr>
            </table>
          </div>
        </div>
        <ui5-tabcontainer fixed collapsed @tab-select="e => changeTab(e.detail.tabIndex)">
          <ui5-tab text="Информация о мероприятии" :selected="selectedTab === 'information'" />
          <ui5-tab text="Расписание" :selected="selectedTab === 'schedule'" />
          <ui5-tab text="Форма заявки пользователя" :selected="selectedTab === 'user_form'" />
          <ui5-tab text="Форма заявки участников от пользователя" :selected="selectedTab === 'part_forms'" />
        </ui5-tabcontainer>
        <div v-if="selectedEvent === null" class="tab-divs">
          <div style="display: inline-block">
            <ui5-badge color-scheme="3">Выберите мероприятие</ui5-badge>
          </div>
        </div>
        <div v-if="selectedEvent !== null" class="tab-divs">
          <div v-if="((selectedTab === 'information') && (Information !== '(информация)'))">
            <ui5-button icon="save"
                        :disabled="changeInfo"
                        @click="e => saveInformation()">
              Сохранить изменения
            </ui5-button><br/><br/>
            <TinyMCE ref='infoTinyMCE'
                     v-bind:Information="Information"
                     v-bind:additional-data="{name: selectedEvent.name}"
                     v-bind:editorHeight="540" />
          </div>
          <div v-if="selectedTab === 'schedule'" class="tab-divs">
            <PaginationTable v-bind:recsURL="'/api/v1/admins/schedule/'+this.selectedEvent.object_id+'/'"
                             v-bind:recAddURL="'/api/v1/admins/schedule_add/'+this.selectedEvent.object_id+'/'"
                             v-bind:recEditURL="'/api/v1/admins/schedule_edit/'"
                             v-bind:recDeleteURL="'/api/v1/admins/schedule_delete/'"
                             v-bind:info="true"
                             v-bind:infoText="'Оранжевым цветом отмечены пересечения по времени'"
                             v-bind:searchRow="false"
                             v-bind:changeShowFields="false"
                             v-bind:colCount="8"
                             v-bind:addButton="true"
                             v-bind:tableColumns="scheduleTableColumns"
                             v-bind:fieldsArray="scheduleFieldsArray"
                             v-bind:dataTableHeight="55"
            />
          </div>
          <div v-if="selectedTab === 'user_form'" class="tab-divs">
            <div style="width: 100%;">
              <table style="margin: 0 auto">
                <tr>
                  <td><ui5-label for="userFormSwitch" show-colon>Используется</ui5-label></td>
                  <td>
                    <ui5-switch ref="userFormSwitch"
                                :checked="eventUserAppRequired"
                                text-off="Нет"
                                text-on="Да"
                                @change="e => changeAppRequired('user_app_required', e.target._state.checked)"
                    />
                  </td>
                </tr>
              </table>
              <div v-if="eventUserAppRequired">
                <ui5-button icon="add" @click="e => eventUserAppFieldAddRow = true">Добавить поле</ui5-button><br/><br/>
                <ui5-table sticky-column-header>
                  <ui5-table-column slot="columns">№</ui5-table-column>
                  <ui5-table-column slot="columns">Наименование поля</ui5-table-column>
                  <ui5-table-column slot="columns">Тип поля</ui5-table-column>
                  <ui5-table-column slot="columns">Допустимые значения</ui5-table-column>
                  <ui5-table-column slot="columns">Управление</ui5-table-column>
                  <ui5-table-row v-if="eventUserAppFieldAddRow">
                    <ui5-table-cell class="additional-row-cell">
                      <ui5-icon class="additional-row-icon" name="add" />
                    </ui5-table-cell>
                    <ui5-table-cell class="additional-row-cell">
                      <ui5-input ref="eventUserAppFieldName" type="Text" />
                    </ui5-table-cell>
                    <ui5-table-cell class="additional-row-cell">
                      <ui5-select v-model="eventUserAppFieldAddType"
                                  @change="e => eventUserAppFieldAddType = e.target.selectedOption.innerText">
                        <ui5-option v-for="field_type in FieldTypes">
                          {{field_type}}
                        </ui5-option>
                      </ui5-select>
                    </ui5-table-cell>
                    <ui5-table-cell class="additional-row-cell">
                      <div v-if="[
                          'Текстовый',
                          'Числовой',
                          'Email',
                          'Номер телефона',
                          'Дата',
                          'Временной интервал (дата-дата)'].includes(eventUserAppFieldAddType)">
                        <b>-</b>
                      </div>
                      <div v-if="['Выбор из списка',
                          'Множественный выбор из списка'].includes(eventUserAppFieldAddType)">
                        <b>Список возможных значений</b>
                      </div>
                      <div v-if="eventUserAppFieldAddType.includes('(из профиля)')">
                        <b>Автоматически</b>
                      </div>
                    </ui5-table-cell>
                    <ui5-table-cell class="additional-row-cell">
                      <ui5-icon interactive
                                class="additional-row-icon"
                                name="accept"
                                @click="e => addAppField(true)"/>
                      &nbsp;&nbsp;
                      <ui5-icon interactive
                                class="additional-row-icon"
                                name="decline"
                                @click="eventUserAppFieldAddRow = false" />
                    </ui5-table-cell>
                  </ui5-table-row>
                  <template v-for="(field, id) in eventUserAppFields">
                    <ui5-table-row v-if="eventUserAppFieldEdit !== field.object_id">
                      <ui5-table-cell>{{id+1}}</ui5-table-cell>
                      <ui5-table-cell>{{field.name}}</ui5-table-cell>
                      <ui5-table-cell>{{field.type}}</ui5-table-cell>
                      <ui5-table-cell>
                        <div v-if="(field.available_values !== null) && (!(field.type.includes('из профиля')))">
                          <br/>
                          <div v-for="value in field.available_values">
                            <ui5-badge  color-scheme="9">
                              {{value}}
                            </ui5-badge><br/><br/>
                          </div>
                        </div>
                        <div v-if="(field.available_values === null) && (field.type.includes('из профиля'))">
                          <b>Автоматически</b>
                        </div>
                        <div v-if="(field.available_values === null) && (!(field.type.includes('из профиля')))">
                          <b>-</b>
                        </div>
                      </ui5-table-cell>
                      <ui5-table-cell>
                        <ui5-icon interactive
                                  name="edit" @click="
                                    eventUserAppFieldEditType = field.type;
                                    eventUserAppFieldEditName = field.name;
                                    eventUserAppFieldEdit = field.object_id" />&nbsp;&nbsp;
                        <ui5-icon interactive
                                  name="delete" @click="deleteAppField(field.object_id, true)" />
                      </ui5-table-cell>
                    </ui5-table-row>
                    <ui5-table-row v-if="eventUserAppFieldEdit === field.object_id">
                      <ui5-table-cell class="additional-row-cell">
                        <ui5-icon class="additional-row-icon" name="edit" />
                      </ui5-table-cell>
                      <ui5-table-cell class="additional-row-cell">
                        <ui5-input v-model="eventUserAppFieldEditName"
                                   type="Text"
                                   @input="e => eventUserAppFieldEditName = e.target.value" />
                      </ui5-table-cell>
                      <ui5-table-cell class="additional-row-cell">
                        <ui5-select @change="e => eventUserAppFieldEditType = e.target.selectedOption.innerText">
                          <ui5-option v-for="field_type in FieldTypes" :selected="field_type === field.type">
                            {{field_type}}
                          </ui5-option>
                        </ui5-select>
                      </ui5-table-cell>
                      <ui5-table-cell class="additional-row-cell">
                        <div v-if="[
                          'Текстовый',
                          'Числовой',
                          'Email',
                          'Номер телефона',
                          'Дата',
                          'Временной интервал (дата-дата)'].includes(eventUserAppFieldEditType)">
                          <b>-</b>
                        </div>
                        <div v-if="['Выбор из списка',
                          'Множественный выбор из списка'].includes(eventUserAppFieldEditType)">
                          <b><ui5-button icon="group-2" @click="e => {
                            selectedFieldID = field.object_id;
                            selectedFieldName = field.name;
                            $refs.fieldAvailableValuesDialog.show(e.target)
                          }">Возможные значения</ui5-button></b>
                        </div>
                        <div v-if="eventUserAppFieldEditType.includes('(из профиля)')">
                          <b>Автоматически</b>
                        </div>
                      </ui5-table-cell>
                      <ui5-table-cell class="additional-row-cell">
                        <ui5-icon interactive
                                  class="additional-row-icon"
                                  name="accept"
                                  @click="e => editAppField(true)"/>
                        &nbsp;&nbsp;
                        <ui5-icon interactive
                                  class="additional-row-icon"
                                  name="decline"
                                  @click="eventUserAppFieldEdit = null" />
                      </ui5-table-cell>
                    </ui5-table-row>
                  </template>
                </ui5-table>
              </div>
            </div>
          </div>
          <div v-if="selectedTab === 'part_forms'" class="tab-divs">
            <div style="width: 100%;">
              <table style="margin: 0 auto">
                <tr>
                  <td><ui5-label for="userFormSwitch" show-colon>Используется</ui5-label></td>
                  <td>
                    <ui5-switch id="userFormSwitch"
                                :checked="eventParticipantAppRequired"
                                text-off="Нет"
                                text-on="Да"
                                @change="e => changeAppRequired('participant_app_required', e.target._state.checked)"
                    />
                  </td>
                </tr>
              </table>
            </div>
            <div v-if="eventParticipantAppRequired">
              <ui5-button icon="add" @click="e => eventParticipantAppFieldAddRow = true">Добавить поле</ui5-button><br/><br/>
              <ui5-table sticky-column-header>
                <ui5-table-column slot="columns">№</ui5-table-column>
                <ui5-table-column slot="columns">Наименование поля</ui5-table-column>
                <ui5-table-column slot="columns">Тип поля</ui5-table-column>
                <ui5-table-column slot="columns">Допустимые значения</ui5-table-column>
                <ui5-table-column slot="columns">Управление</ui5-table-column>
                <ui5-table-row v-if="eventParticipantAppFieldAddRow">
                  <ui5-table-cell class="additional-row-cell">
                    <ui5-icon class="additional-row-icon" name="add" />
                  </ui5-table-cell>
                  <ui5-table-cell class="additional-row-cell">
                    <ui5-input ref="eventParticipantAppFieldName" type="Text" />
                  </ui5-table-cell>
                  <ui5-table-cell class="additional-row-cell">
                    <ui5-select v-model="eventParticipantAppFieldAddType"
                                @change="e => eventParticipantAppFieldAddType = e.target.selectedOption.innerText">
                      <ui5-option v-for="field_type in FieldTypes">
                        {{field_type}}
                      </ui5-option>
                    </ui5-select>
                  </ui5-table-cell>
                  <ui5-table-cell class="additional-row-cell">
                    <div v-if="[
                          'Текстовый',
                          'Числовой',
                          'Email',
                          'Номер телефона',
                          'Дата',
                          'Временной интервал (дата-дата)'].includes(eventParticipantAppFieldAddType)">
                      <b>-</b>
                    </div>
                    <div v-if="['Выбор из списка',
                          'Множественный выбор из списка'].includes(eventParticipantAppFieldAddType)">
                      <b>Список возможных значений</b>
                    </div>
                    <div v-if="eventParticipantAppFieldAddType.includes('(из профиля)')">
                      <b>Автоматически</b>
                    </div>
                  </ui5-table-cell>
                  <ui5-table-cell class="additional-row-cell">
                    <ui5-icon interactive
                              class="additional-row-icon"
                              name="accept"
                              @click="e => addAppField(false)"/>
                    &nbsp;&nbsp;
                    <ui5-icon interactive
                              class="additional-row-icon"
                              name="decline"
                              @click="eventParticipantAppFieldAddRow = false" />
                  </ui5-table-cell>
                </ui5-table-row>
                <template v-for="(field, id) in eventParticipantAppFields">
                  <ui5-table-row v-if="eventParticipantAppFieldEdit !== field.object_id">
                    <ui5-table-cell>{{id+1}}</ui5-table-cell>
                    <ui5-table-cell>{{field.name}}</ui5-table-cell>
                    <ui5-table-cell>{{field.type}}</ui5-table-cell>
                    <ui5-table-cell>
                      <div v-if="(field.available_values !== null) && (!(field.type.includes('из профиля')))">
                        <br/>
                        <div v-for="value in field.available_values">
                          <ui5-badge  color-scheme="9">
                            {{value}}
                          </ui5-badge><br/><br/>
                        </div>
                      </div>
                      <div v-if="(field.available_values === null) && (field.type.includes('из профиля'))">
                        <b>Автоматически</b>
                      </div>
                      <div v-if="(field.available_values === null) && (!(field.type.includes('из профиля')))">
                        <b>-</b>
                      </div>
                    </ui5-table-cell>
                    <ui5-table-cell>
                      <ui5-icon interactive
                                name="edit" @click="
                                    eventParticipantAppFieldEditType = field.type;
                                    eventParticipantAppFieldEditName = field.name;
                                    eventParticipantAppFieldEdit = field.object_id" />&nbsp;&nbsp;
                      <ui5-icon interactive
                                name="delete" @click="deleteAppField(field.object_id, false)" />
                    </ui5-table-cell>
                  </ui5-table-row>
                  <ui5-table-row v-if="eventParticipantAppFieldEdit === field.object_id">
                    <ui5-table-cell class="additional-row-cell">
                      <ui5-icon class="additional-row-icon" name="edit" />
                    </ui5-table-cell>
                    <ui5-table-cell class="additional-row-cell">
                      <ui5-input v-model="eventParticipantAppFieldEditName"
                                 type="Text"
                                 @input="e => eventParticipantAppFieldEditName = e.target.value" />
                    </ui5-table-cell>
                    <ui5-table-cell class="additional-row-cell">
                      <ui5-select @change="e => eventParticipantAppFieldEditType = e.target.selectedOption.innerText">
                        <ui5-option v-for="field_type in FieldTypes" :selected="field_type === field.type">
                          {{field_type}}
                        </ui5-option>
                      </ui5-select>
                    </ui5-table-cell>
                    <ui5-table-cell class="additional-row-cell">
                      <div v-if="[
                          'Текстовый',
                          'Числовой',
                          'Email',
                          'Номер телефона',
                          'Дата',
                          'Временной интервал (дата-дата)'].includes(eventParticipantAppFieldEditType)">
                        <b>-</b>
                      </div>
                      <div v-if="['Выбор из списка',
                          'Множественный выбор из списка'].includes(eventParticipantAppFieldEditType)">
                        <b><ui5-button icon="group-2" @click="e => {
                            selectedFieldID = field.object_id;
                            selectedFieldName = field.name;
                            $refs.fieldAvailableValuesDialog.show(e.target)
                          }">Возможные значения</ui5-button></b>
                      </div>
                      <div v-if="eventParticipantAppFieldEditType.includes('(из профиля)')">
                        <b>Автоматически</b>
                      </div>
                    </ui5-table-cell>
                    <ui5-table-cell class="additional-row-cell">
                      <ui5-icon interactive
                                class="additional-row-icon"
                                name="accept"
                                @click="e => editAppField(false)"/>
                      &nbsp;&nbsp;
                      <ui5-icon interactive
                                class="additional-row-icon"
                                name="decline"
                                @click="eventParticipantAppFieldEdit = null" />
                    </ui5-table-cell>
                  </ui5-table-row>
                </template>
              </ui5-table>
            </div>
          </div>
        </div>
      </ui5-card>
    </slot>
  </LkBase>
  <ui5-dialog ref="findEventDialog">
    <AdminEventsTable v-bind:tableColumns="eventSearchTableColumns"
                      v-bind:headerText="'Поиск мероприятия'"
                      v-bind:tableMode="'SingleSelect'"
                      v-bind:addButton="false"
                      v-bind:activeRow="'Active'"
                      v-bind:activeRowEvent="setSelectedEvent"
                      v-bind:showActions="true"/>
    <div slot="footer" style="display: flex; justify-content: flex-end; width: 100%; align-items: center">
      <div style="flex: 1;"></div>
      <ui5-button design="Emphasized"
                  @click="e => $refs.findEventDialog.close()">
        Закрыть
      </ui5-button>
    </div>
  </ui5-dialog>
  <ui5-dialog ref="fieldAvailableValuesDialog" style="width: 50vw;">
    Список возможных значений для поля "<b>{{selectedFieldName}}</b>"<br/><br/>
    <PaginationTable v-if="selectedFieldID !== null"
                     v-bind:recsURL="'/api/v1/applications/available_values/'+this.selectedFieldID+'/'"
                     v-bind:recAddURL="'/api/v1/applications/available_value_add/'+this.selectedFieldID+'/'"
                     v-bind:recEditURL="'/api/v1/applications/available_value_edit/'"
                     v-bind:recDeleteURL="'/api/v1/applications/available_value_delete/'"
                     v-bind:searchRow="false"
                     v-bind:changeShowFields="false"
                     v-bind:colCount="3"
                     v-bind:activeRow="'Inactive'"
                     v-bind:addButton="true"
                     v-bind:tableColumns="[
                         {name: 'ID объекта', alias: 'object_id', whiteSpace: 'nowrap'},
                         {name: 'Вариант ответа', alias: 'option', whiteSpace: 'nowrap'},
                         {name: 'Действия', alias: 'actions', whiteSpace: 'nowrap'},
                     ]"
                     v-bind:fieldsArray="[
                        {
                          ui: 'None',
                          field: 'object_id',
                        },
                        {
                          ui: 'input',
                          type: 'Text',
                          field: 'option',
                          add_required: true
                        },
                        {
                          ui: 'icon',
                          field: 'actions'
                        }
                     ]"
                     v-bind:dataTableHeight="60"
    />
    <div slot="footer" style="display: flex; justify-content: flex-end; width: 100%; align-items: center">
      <ui5-button design="Emphasized" @click="e => {
        selectedFieldID = null;
        $refs.fieldAvailableValuesDialog.close()
      }">
        Закрыть
      </ui5-button>
    </div>
  </ui5-dialog>
</template>

<script>
import LkBase from "../../../components/LkBase.vue";
import PaginationTable from "../../../components/PaginationTable.vue";
import AdminEventsTable from "./AdminEventsTable.vue";
import TinyMCE from "../../../components/TinyMCE.vue";
import app_form_field_types from "../../../consts/app_form_field_types.js";

export default {
  name: 'AdminEventsManage',
  components: {TinyMCE, AdminEventsTable, LkBase, PaginationTable},
  data() {
    return {
      Information: '(информация)',
      eventSchedule: [],
      changeInfo: false,
      selectedTab: 'information',
      selectedEvent: null,
      eventSearchTableColumns: [
        {name: 'ID объекта', alias: 'object_id', whiteSpace: 'nowrap'},
        {name: 'Наименование', alias: 'name', whiteSpace: 'nowrap'},
        {name: 'Краткое пояснение', alias: 'description', whiteSpace: 'normal'},
        {name: 'Тип', alias: 'event_type', whiteSpace: 'normal'},
        {name: 'Сроки подачи заявок', alias: 'app_date_range', whiteSpace: 'nowrap'},
        {name: 'Сроки проведения мероприятия', alias: 'date_range', whiteSpace: 'nowrap'},
        {name: 'Категории участников', alias: 'categories', whiteSpace: 'nowrap'}
      ],
      scheduleTableColumns: [
        {name: 'ID объекта', alias: 'object_id', whiteSpace: 'nowrap'},
        {name: 'Время начала', alias: 'start', whiteSpace: 'nowrap'},
        {name: 'Время окончания', alias: 'end', whiteSpace: 'nowrap'},
        {name: 'Тема', alias: 'theme', whiteSpace: 'normal'},
        {name: 'Формат проведения', alias: 'form', whiteSpace: 'nowrpap'},
        {name: 'Ссылка', alias: 'url', whiteSpace: 'normal'},
        {name: 'Адрес', alias: 'address', whiteSpace: 'normal'},
        {name: 'Действия', alias: 'actions'}
      ],
      scheduleFieldsArray: [],
      FieldTypes: app_form_field_types,
      eventUserAppRequired: false,
      eventUserAppFields: [],
      eventUserAppFieldAddRow: false,
      eventUserAppFieldAddType: 'Текстовый',
      eventUserAppFieldEditName: '',
      eventUserAppFieldEditType: 'Текстовый',
      eventUserAppFieldEdit: null,

      eventParticipantAppRequired: false,
      eventParticipantAppFields: [],
      eventParticipantAppFieldAddRow: false,
      eventParticipantAppFieldAddType: 'Текстовый',
      eventParticipantAppFieldEditName: '',
      eventParticipantAppFieldEditType: 'Текстовый',
      eventParticipantAppFieldEdit: null,

      selectedFieldID: null,
      selectedFieldName: '',
    }
  },
  methods: {
    async getForms() {
      await fetch(this.$store.state.backendUrl+'/api/v1/admins/events_forms/', {
        method: 'GET',
        headers: {
          'X-CSRFToken': getCookie("csrftoken"),
          'Content-Type': 'web_app/json;charset=UTF-8',
          'Authorization': 'Token '+getCookie('iohk_token')
        },
      })
          .then(resp => {
            if (resp.status === 200) {
              return resp.json()
            } else {
              showMessage('error', 'Произошла ошибка при получении форм проведения мероприятия, повторите попытку позже')
              return false
            }
          })
          .then(data => {
            let forms = [{id: 0, name: ''}]
            data.map((form, id) => {
              forms.push({id: id, name: form.name})
            })
            this.scheduleFieldsArray = [
              {
                ui: 'None',
                field: 'object_id',
              },
              {
                ui: 'datetime_picker',
                field: 'start',
                add_required: true
              },
              {
                ui: 'datetime_picker',
                field: 'end',
                add_required: true
              },
              {
                ui: 'input',
                type: 'Text',
                field: 'theme',
                add_required: true
              },
              {
                ui: 'select',
                options: forms,
                field: 'form',
                add_required: true
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
              {
                ui: 'icon',
                field: 'actions'
              }
            ]
          })
    },
    setSelectedEvent(event) {
      this.selectedEvent = event
      this.selectedTab = ''
      this.getEventInformation()
      this.$refs.findEventDialog.close()
    },
    async saveInformation() {
      this.changeInfo = true
      let url = this.$store.state.backendUrl+'/api/v1/admins/information_save/'+this.selectedEvent.object_id+'/'
      await fetch (url,{
        method: 'PATCH',
        headers: {
          'X-CSRFToken': getCookie('csrftoken'),
          'Content-Type': 'web_app/json;charset=UTF-8',
          'Authorization': 'Token '+getCookie('iohk_token')
        },
        body: JSON.stringify({
          'info': this.$refs.infoTinyMCE.editorText
        })
      })
          .then(resp => {
            if (resp.status === 200) {
              return resp.json()
            } else {
              this.changeInfo = false
              if (resp.status === 401) {
                showMessage('error', 'Пожалуйста, войдите в систему', false)
                this.$router.push('/?nextUrl='+window.location.href.split('/')[3])
                return false
              }
              showMessage('error', 'Произошла ошибка, повторите попытку позже')
            }
          })
          .then(data => {
            if (data['error']) {
              showMessage('error', data['error'])
            } else {
              showMessage('success', data['success'])
              this.getEventInformation()
            }
            this.changeInfo = false
          })
    },
    changeTab(index) {
      switch(index) {
        case 0:
          this.getEventInformation()
          this.selectedTab = 'information'
          break

        case 1:
          this.getSchedule()
          this.selectedTab = 'schedule'
          break

        case 2:
          this.getAppsRequired()
          this.getAppFields('user_app')
          this.selectedTab = 'user_form'
          break

        default:
          this.getAppsRequired()
          this.getAppFields('part_app')
          this.selectedTab = 'part_forms'
      }
    },
    async getEventInformation() {
      await fetch(this.$store.state.backendUrl+'/api/v1/admins/information/?event='+this.selectedEvent.name, {
        method: 'GET',
        headers: {
          'X-CSRFToken': getCookie("csrftoken"),
          'Content-Type': 'web_app/json;charset=UTF-8',
          'Authorization': 'Token '+getCookie('iohk_token')
        },
      })
          .then(resp => {
            if (resp.status === 200) {
              return resp.json()
            } else {
              showMessage('error', 'Произошла ошибка при получении информации о мероприятии, повторите попытку позже')
              return false
            }
          })
          .then(data => {
            this.Information = data[0]['info']
            this.selectedTab = 'information'
          })
    },
    async getSchedule() {
      let url = this.$store.state.backendUrl+'/api/v1/admins/schedule/'+this.selectedEvent.object_id+'/'
      await fetch(url, {
        method: 'GET',
        headers: {
          'X-CSRFToken': getCookie("csrftoken"),
          'Content-Type': 'web_app/json;charset=UTF-8',
          'Authorization': 'Token '+getCookie('iohk_token')
        },
      })
          .then(resp => {
            if (resp.status === 200) {
              return resp.json()
            } else {
              showMessage('error', 'Произошла ошибка при получении расписания, повторите попытку позже')
              return false
            }
          })
          .then(data => {
            this.eventSchedule = data
            changeTableView()
          })
    },
    async getAppsRequired() {
      let url = this.$store.state.backendUrl+'/api/v1/admins/apps_required/'+this.selectedEvent.object_id+'/'
      await fetch(url, {
        method: 'GET',
        headers: {
          'X-CSRFToken': getCookie("csrftoken"),
          'Content-Type': 'web_app/json;charset=UTF-8',
          'Authorization': 'Token '+getCookie('iohk_token')
        },
      })
          .then(resp => {
            if (resp.status === 200) {
              return resp.json()
            } else {
              showMessage('error', 'Произошла ошибка, повторите попытку позже')
              return false
            }
          })
          .then(data => {
            this.eventUserAppRequired = data['user_app_required']
            this.eventParticipantAppRequired = data['participant_app_required']
          })
    },
    async changeAppRequired(type, value) {
      if (type === 'user_app_required') {
        this.eventUserAppRequired = value
        await this.getAppFields('user_app')
      } else {
        this.eventParticipantAppRequired = value
        await this.getAppFields('participant_app')
      }
      await fetch (this.$store.state.backendUrl+'/api/v1/admins/apps_required_edit/',{
        method: 'POST',
        headers: {
          'X-CSRFToken': getCookie('csrftoken'),
          'Content-Type': 'web_app/json;charset=UTF-8',
          'Authorization': 'Token '+getCookie('iohk_token')
        },
        body: JSON.stringify({
          'event_id': this.selectedEvent.object_id,
          'type': type,
          'value': value
        })
      })
          .then(resp => {
            if (resp.status === 401) {
              showMessage('error', 'Пожалуйста, войдите в систему', false)
              this.$router.push('/?nextUrl='+window.location.href.split('/')[3])
              return false
            } else {
              return true
            }
          })
    },
    async getAppFields(type) {
      let url = this.$store.state.backendUrl+'/api/v1/admins/app_fields/'+this.selectedEvent.object_id+'/'+type+'/'
      await fetch(url, {
        method: 'GET',
        headers: {
          'X-CSRFToken': getCookie("csrftoken"),
          'Content-Type': 'web_app/json;charset=UTF-8',
          'Authorization': 'Token '+getCookie('iohk_token')
        },
      })
          .then(resp => {
            if (resp.status === 200) {
              return resp.json()
            } else {
              showMessage('error', 'Произошла ошибка при получении полей заявки, повторите попытку позже')
              return false
            }
          })
          .then(data => {
            if (type === 'user_app') {
              this.eventUserAppFields = data
            } else {
              this.eventParticipantAppFields = data
            }
            setTimeout(changeTableView, 25)
          })
    },
    async addAppField(user_app) {
      let data = {
        'event': this.selectedEvent.object_id,
        'user_app': user_app
      }
      if (user_app) {
        data['name'] = this.$refs.eventUserAppFieldName.value
        data['type'] = this.eventUserAppFieldAddType
      } else {
        data['name'] = this.$refs.eventParticipantAppFieldName.value
        data['type'] = this.eventParticipantAppFieldAddType
      }
      await fetch (this.$store.state.backendUrl+'/api/v1/admins/app_field_new/',{
        method: 'POST',
        headers: {
          'X-CSRFToken': getCookie('csrftoken'),
          'Content-Type': 'web_app/json;charset=UTF-8',
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
              if (user_app) {
                this.getAppFields('user_app')
              } else {
                this.getAppFields('part_app')
              }
            }
          })
    },
    async editAppField(user_app) {
      let url = this.$store.state.backendUrl+'/api/v1/admins/app_field_edit/'
      let data = {
        'event': this.selectedEvent.object_id,
        'user_app': user_app
      }
      if (user_app) {
        data['name'] = this.eventUserAppFieldEditName
        data['type'] = this.eventUserAppFieldEditType
        url += this.eventUserAppFieldEdit+'/'
      } else {
        data['name'] = this.eventParticipantAppFieldEditName
        data['type'] = this.eventParticipantAppFieldEditType
        url += this.eventParticipantAppFieldEdit+'/'
      }
      await fetch (url,{
        method: 'PATCH',
        headers: {
          'X-CSRFToken': getCookie('csrftoken'),
          'Content-Type': 'web_app/json;charset=UTF-8',
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
              if (user_app) {
                this.getAppFields('user_app')
              } else {
                this.getAppFields('part_app')
              }
            }
          })
    },
    async deleteAppField(field_id, user_app) {
      if (confirm('Вы уверены, что хотите удалить поле?')) {
        await fetch (this.$store.state.backendUrl+'/api/v1/admins/app_field_delete/'+field_id+'/',{
          method: 'DELETE',
          headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'web_app/json;charset=UTF-8',
            'Authorization': 'Token '+getCookie('iohk_token')
          }
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
                if (user_app) {
                  this.getAppFields('user_app')
                } else {
                  this.getAppFields('part_app')
                }

              }
            })
      }
    }
  },
  mounted() {
    this.getForms()
  }
}
</script>

<style scoped>
  .tab-divs {
    width: 100%;
    text-align: center;
    justify-content: center;
    height: 65vh;
    overflow: auto;
  }

</style>