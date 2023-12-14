<template>
  <LkBase ref="baseComponent">
    <slot>
      <ui5-card class="full-card">
        <ui5-card-header slot="header"
                         title-text="Справочники">
        </ui5-card-header>
        <ui5-tabcontainer fixed collapsed @tab-select="e => changeTab(e.detail.tabIndex)">
          <ui5-tab text="Типы мероприятий" :selected="selectedTab === 'event_types'" />
          <ui5-tab text="Категории участников" :selected="selectedTab === 'participant_categories'" />
          <ui5-tab text="Формы проведения" :selected="selectedTab === 'event_forms'" />
        </ui5-tabcontainer><br/><br/>
        <EventsTypes v-if="selectedTab === 'event_types'" />
        <ParticipantCategories v-if="selectedTab === 'participant_categories'" />
        <EventsForms v-if="selectedTab === 'event_forms'" />
      </ui5-card>
    </slot>
  </LkBase>
</template>

<script>
import LkBase from "../../components/LkBase.vue";
import EventsTypes from "./guides/EventsTypes.vue";
import ParticipantCategories from "./guides/ParticipantCategories.vue";
import EventsForms from "./guides/EventsForms.vue";

export default {
  name: 'Guides',
  components: {EventsForms, ParticipantCategories, EventsTypes, LkBase},
  data() {
    return {
      selectedTab: 'event_types',
    }
  },
  methods: {
    changeTab(tab_index) {
      switch (tab_index) {
        case 0:
          this.selectedTab = 'event_types'
          break

        case 1:
          this.selectedTab = 'participant_categories'
          break

        default:
          this.selectedTab = 'event_forms'
      }
    }
  }
}
</script>

<style scoped>

</style>