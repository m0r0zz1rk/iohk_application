<template>
  <div class="main-content">
    <router-view/>
    <div v-if="preLoader" class="loader-container">
      <span class="loader"></span>
    </div>
  </div>
</template>

<script>

export default {
  name: 'PreLoader',
  data() {
    return {
      preLoader: false
    }
  },
  methods: {
    usePreloader(onlyClose = false) {
      if (this.preLoader) {
        this.preLoader = false
      } else {
        if (!(onlyClose)) {
          if (!(this.preLoader)) {
            this.preLoader = true
          }
        }
      }
    }
  }
}
</script>

<style>
.full-card {
  height: calc(95vh - 80px);
  width: 98%;
  overflow: auto;
}
.main-content {
  position: absolute;
  top: 0;
  right: 0;
  width: 100vw;
  height: 100vh;
  overflow: hidden;
  --sapButton_Lite_TextColor: #cb5b11;
  --sapAvatar_1_Background: #00455d;
  --sapAvatar_1_BorderColor: #00455d;
  --sapAvatar_1_TextColor: #ffffff;
}
.loader-container {
  position: absolute;
  top: 0;
  right: 0;
  width: 100vw;
  height: 100vh;
  background-color: #00455d;
  z-index: 20;
}
.loader {
  transform: rotateZ(45deg);
  perspective: 1000px;
  border-radius: 50%;
  width: 48px;
  height: 48px;
  color: #fff;
  z-index: 20;
  position: absolute;
  top: calc(50% - 48px);
  left: calc(50% - 48px);
}
.loader:before,
.loader:after {
  content: '';
  display: block;
  position: absolute;
  top: 0;
  left: 0;
  width: inherit;
  height: inherit;
  border-radius: 50%;
  transform: rotateX(70deg);
  animation: 1s spin linear infinite;
}
.loader:after {
  color: #e85c00;
  transform: rotateY(70deg);
  animation-delay: .4s;
}

@keyframes rotate {
  0% {
    transform: translate(-50%, -50%) rotateZ(0deg);
  }
  100% {
    transform: translate(-50%, -50%) rotateZ(360deg);
  }
}

@keyframes rotateccw {
  0% {
    transform: translate(-50%, -50%) rotate(0deg);
  }
  100% {
    transform: translate(-50%, -50%) rotate(-360deg);
  }
}

@keyframes spin {
  0%,
  100% {
    box-shadow: .2em 0px 0 0px currentcolor;
  }
  12% {
    box-shadow: .2em .2em 0 0 currentcolor;
  }
  25% {
    box-shadow: 0 .2em 0 0px currentcolor;
  }
  37% {
    box-shadow: -.2em .2em 0 0 currentcolor;
  }
  50% {
    box-shadow: -.2em 0 0 0 currentcolor;
  }
  62% {
    box-shadow: -.2em -.2em 0 0 currentcolor;
  }
  75% {
    box-shadow: 0px -.2em 0 0 currentcolor;
  }
  87% {
    box-shadow: .2em -.2em 0 0 currentcolor;
  }
}

</style>