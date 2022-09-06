<template>
         <footer class="footer">
          <div class="container-fluid">
            <nav>
              <ul class="nav">
                <li class="nav-item">
                  <p>
                      pyb0987@naver.com
                  </p>
                </li>
                <li class="nav-item">
                  <a
                    href="https://github.com/pyb0987"
                    target="_blank"
                    rel="noopener"
                    class="nav-link"
                  >
                    github
                  </a>
                </li>
              </ul>
            </nav>
            <div class="copyright">
              &copy; {{ year }} Seoulbike
            </div>
          </div>
        </footer>
</template>
<script>
export default {
  data() {
    return {
      year: new Date().getFullYear()
    };
  }
};
</script>
<style></style>
