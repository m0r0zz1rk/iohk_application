<template>
  <LkBase ref="baseComponent">
    <slot>
      <ui5-card class="full-card">
        <ui5-card-header slot="header"
                         title-text="Мероприятия">
        </ui5-card-header>
        <ui5-tabcontainer v-if="eventsTypes.length > 0"
                          fixed
                          collapsed
                          @tab-select="e => changeTab(e.detail.tabIndex)">
          <ui5-tab v-for="(type, id) in eventsTypes"
                   :text="type.name_plural"
                   :selected="selectedTab === id" />
        </ui5-tabcontainer><br/><br/>
        <div v-if="loader" style="width: 50%; margin: 0 auto">
          <ui5-message-strip design="Warning" hideCloseButton>
            <img src="/media/gifs/loading.gif" alt="Подождите" width="16" height="16" slot="icon" />
            Пожалуйста, подождите...
          </ui5-message-strip>
        </div>
        <EventsGrid v-if="events.length > 0"
                    v-bind:showDetailsFunction="showEventDetails"
                    v-bind:eventsList="events" />
      </ui5-card>
    </slot>
  </LkBase>
  <ui5-dialog ref="eventDetailDialog" style="z-index: 16" draggable>
    <ui5-bar slot="header">
      <ui5-title level="H5" slot="startContent">Детальная информация о мероприятии</ui5-title>
      <ui5-button design="Emphasized" slot="endContent" icon="decline" @click="e => this.$refs.eventDetailDialog.close(e.current)"></ui5-button>
    </ui5-bar>
    <div v-if="selectedEvent.loading" style="margin: 0 auto">
      <ui5-message-strip design="Warning" hideCloseButton>
        <img src="/media/gifs/loading.gif" alt="Подождите" width="16" height="16" slot="icon" />
        Пожалуйста, подождите...
      </ui5-message-strip>
    </div>
    <div v-if="!(selectedEvent.loading)">
      <ui5-tabcontainer fixed
                        collapsed
                        @tab-select="e => changeEventTab(e.detail.tabIndex)">
        <ui5-tab text="Информационное сообщение" :selected="selectedEvent.tab === 'info'" />
        <ui5-tab text="Расписание" :selected="selectedEvent.tab === 'schedule'" />
      </ui5-tabcontainer><br/><br/>
      <div style="width: 80vw; height: 65vh; overflow-x: auto">
        <div v-if="selectedEvent.tab === 'info'" v-html="selectedEvent.info" />
        <div v-if="selectedEvent.tab === 'schedule'">
          <PaginationTable v-bind:recsURL="'/api/v1/users/event_schedule/'+this.selectedEvent.id+'/'"
                           v-bind:info="true"
                           v-bind:infoText="'Оранжевым цветом отмечены пересечения по времени'"
                           v-bind:searchRow="false"
                           v-bind:changeShowFields="false"
                           v-bind:colCount="8"
                           v-bind:addButton="false"
                           v-bind:tableColumns="scheduleTableColumns"
                           v-bind:dataTableHeight="55"
          />
        </div>
      </div>

    </div>
    <div slot="footer" style="display: flex; justify-content: flex-end; width: 100%; align-items: center">
      <form v-if="!(selectedEvent.app_exists)" ref="login_form"  @submit="eventAppCreate">
        <ui5-button design="Emphasized" submits>Подать заявку</ui5-button>
      </form>
      <ui5-button v-if="selectedEvent.app_exists"
                  @click="e => $router.push('/apps/app_detail/'+selectedEvent.id+'/')"
                  design="Emphasized">
        Открыть заявку
      </ui5-button>
    </div>
  </ui5-dialog>
</template>

<script>
import LkBase from "../../components/LkBase.vue";
import {apiRequest} from "../../additional/functions/api_request.js";
import EventsGrid from "../../components/EventsGrid.vue";
import PaginationTable from "../../components/PaginationTable.vue";

export default {
  name: 'Events',
  components: {PaginationTable, EventsGrid, LkBase},
  data() {
    return {
      loader: false,
      eventsTypes: [],
      events: [],
      content: '',
      selectedTab: 'event_types',
      scheduleTableColumns: [
        {name: 'ID объекта', alias: 'object_id', whiteSpace: 'nowrap'},
        {name: 'Время начала', alias: 'start', whiteSpace: 'nowrap'},
        {name: 'Время окончания', alias: 'end', whiteSpace: 'nowrap'},
        {name: 'Тема', alias: 'theme', whiteSpace: 'normal'},
        {name: 'Формат проведения', alias: 'form', whiteSpace: 'nowrpap'},
        {name: 'Ссылка', alias: 'url', whiteSpace: 'normal'},
        {name: 'Адрес', alias: 'address', whiteSpace: 'normal'}
      ],
      selectedEvent: {
        loading: true,
        app_exists: false,
        tab: 'info',
        id: '',
        info: '',
        schedule: []
      }
    }
  },
  methods: {
    async init() {
      apiRequest(
          this.$store.state.backendUrl+'/api/v1/users/event_types/',
          'GET',
          true,
          null,
          false,
          false
      )
          .then(data => {
            this.eventsTypes = data
            this.getEventsByType(this.eventsTypes[0].name)
          })
    },
    changeTab(tab_index) {
      this.getEventsByType(this.eventsTypes[tab_index].name)
    },
    async getEventsByType(event_type) {
      this.loader = true
      apiRequest(
          this.$store.state.backendUrl+'/api/v1/users/events/?event_type='+event_type,
          'GET',
          true,
          null,
          false,
          false
      )
          .then(data => {
            this.events = data
            this.loader = false
          })
    },
    showEventDetails(e, id) {
      this.selectedEvent.loading = true
      this.selectedEvent.id = id
      this.checkAppExists()
      this.changeEventTab(0)
      this.getEventInfo()
      this.$refs.eventDetailDialog.show(e.current)
    },
    changeEventTab(index) {
      switch (index) {
        case 0:
          this.selectedEvent.tab = 'info'
          break

        default:
          this.selectedEvent.tab = 'schedule'
      }
    },
    async checkAppExists() {
      apiRequest(
          this.$store.state.backendUrl+'/api/v1/users/apps/check_exist/'+this.selectedEvent.id+'/',
          'GET',
          true,
          null,
          false,
          true
      )
          .then(resp => {
            if (resp.status === 200) {
              this.selectedEvent.app_exists = true
            } else {
              this.selectedEvent.app_exists = false
            }
          })
    },
    async getEventInfo() {
      apiRequest(
          this.$store.state.backendUrl+'/api/v1/users/event_info/'+this.selectedEvent.id+'/',
          'GET',
          true,
          null,
          false,
          false
      )
          .then(data => {
            this.selectedEvent.info = data.info
            this.selectedEvent.loading = false
          })
    },
    async eventAppCreate(e) {
      e.preventDefault()
    },

  },
  mounted() {
    this.init()
  }
}
</script>

<style scoped>

</style>