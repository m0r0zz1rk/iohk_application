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
          <ui5-message-strip design="Warning"  hideCloseButton>
            <img src="/media/gifs/loading.gif" alt="Подождите" width="16" height="16" slot="icon" />
            Пожалуйста, подождите...
          </ui5-message-strip>
        </div>
        <EventsGrid v-if="events.length > 0" v-bind:eventsList="events" />
      </ui5-card>
    </slot>
  </LkBase>
</template>

<script>
import LkBase from "../../components/LkBase.vue";
import {apiRequest} from "../../additional/functions/api_request.js";
import EventsGrid from "../../components/EventsGrid.vue";

export default {
  name: 'Events',
  components: {EventsGrid, LkBase},
  data() {
    return {
      loader: false,
      eventsTypes: [],
      events: [],
      content: '',
      selectedTab: 'event_types',
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
    }
  },
  mounted() {
    this.init()
  }
}
</script>

<style scoped>

</style>