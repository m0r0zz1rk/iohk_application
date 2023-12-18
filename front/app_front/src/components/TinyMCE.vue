<template>
  <Editor v-if="editorText.length > 0"
      v-model="editorText"
      :api-key="TinyMCEAPIKey"
      :init="{
         height: editorHeight,
         menubar: 'edit table',
         language: 'ru',
         plugins: [
           'advlist autolink lists link image charmap print preview anchor',
           'searchreplace visualblocks code fullscreen',
           'insertdatetime media table paste code help wordcount'
         ],
         toolbar:
           'undo redo | bold italic underline strikethrough | \
           fontselect fontsizeselect formatselect | \
           alignleft aligncenter alignright alignjustify | \
           outdent indent |  numlist bullist checklist | \
           forecolor backcolor casechange permanentpen formatpainter removeformat | \
           pagebreak | charmap emoticons | preview save | \
           insertfile image pageembed template link codesample | \
           a11ycheck ltr rtl',
         images_upload_handler: (blobInfo, success, failure) => {
            imagesUploadHandler(blobInfo, success, failure)
         }
      }"
  />
</template>

<script>
import Editor from '@tinymce/tinymce-vue'

export default {
  name: 'TinyMCE',
  components: {Editor},
  props: {
    Information: {type: String},
    additionalData: {type: Object},
    editorHeight: {type: Number}
  },
  data() {
    return {
      editorText: '',
      TinyMCEAPIKey: import.meta.env.VITE_APP_TINYMCE_API_KEY
    }
  },
  methods: {
    init() {
      this.editorText = this.Information
    },
    async imagesUploadHandler(blobInfo, success, failure) {
      let formRequest = new FormData()
      formRequest.append('file', blobInfo.blob(), blobInfo.filename())
      formRequest.append('name', this.additionalData['name'])
      await fetch (this.$store.state.backendUrl+'/api/v1/commons/tinymce_image/', {
        method: 'PUT',
        headers: {
          'X-CSRFToken': getCookie('csrftoken'),
          'Authorization': 'Token '+getCookie('iohk_token')
        },
        body: formRequest
      })
          .then(resp => resp.json())
          .then(data => {
            if (data.location) {
              success(this.$store.state.backendUrl+data.location)
            } else {
              failure(data.error)
            }
          })
    }
  },
  beforeMount() {
    this.init()
  }
}
</script>

<style scoped>

</style>