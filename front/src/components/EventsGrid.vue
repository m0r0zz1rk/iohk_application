<template>
  <div style="height: 70vh; overflow: auto">
    <div class="grid-container grid-container-adaptive">
      <ui5-card v-for="event in eventsList" >
        <ui5-card-header slot="header"
                         :title-text="event.name">
        </ui5-card-header>
        <div class="content content-padding">
          <div class="content-group">
            <ui5-label>Краткое описание</ui5-label>
            <ui5-title level="H6">{{ event.description }}</ui5-title>
          </div>
          <div class="content-group">
            <ui5-label>Сроки подачи заявок</ui5-label>
            <ui5-title level="H6">{{ event.app_date_range }}</ui5-title>
          </div>
          <div class="content-group">
            <ui5-label>Сроки проведения</ui5-label>
            <ui5-title level="H6">
              {{ event.date_range }}
            </ui5-title>
          </div>
          <div class="content-group">
            <ui5-label>Категории участников</ui5-label>
            <ui5-title level="H6">
              <div style="display: inline-block" v-for="cat in event.categories">
                <ui5-badge  color-scheme="6">
                  {{cat}}
                </ui5-badge>&nbsp;
              </div>
            </ui5-title>
          </div>
        </div>
        <div class="card-center-button-div">
          <ui5-button style="margin: 0 auto;"
                      icon="business-card"
                      @click="e => showDetailsFunction(e, event.object_id)">Подробнее</ui5-button>
        </div>
      </ui5-card>
    </div>
  </div>

</template>

<script>
export default {
  name: 'EventsGrid',
  props: {
    eventsList: {type: Array},
    showDetailsFunction: {type: Function}
  },
}
</script>

<style scoped>
.grid-container {
  padding-left: 10px;
  display: grid;
  width: 97%;
}
.content,
.content-group {
  display: flex;
  flex-direction: column;
  padding-block-end: 1rem;
}
.content-padding {
  padding: 0.5rem 1rem 0 1rem;
  box-sizing: border-box;
}
.card-center-button-div {
  display: flex;
  width: 100%;
  margin: 0 auto;
  justify-content: center;
  padding-bottom: 15px;
  padding-top: 15px;
}
</style>