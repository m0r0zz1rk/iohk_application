<template>
  <ui5-badge v-if="sex" color-scheme="6">Мужчина</ui5-badge>
  <ui5-badge v-if="!(sex)" color-scheme="2">Женщина</ui5-badge>
</template>

<script>
export default {
  name: 'SexBadge',
  props: {
    sex: {type: Boolean}
  }
}

</script>

<style scoped>

</style>