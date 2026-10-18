pluginManagement {
    repositories {
        gradlePluginPortal()
        mavenCentral()
    }
}

rootProject.name = "TanLekun-TanBengjin"

includeBuild("KonvertLegacyPOJ") {
    dependencySubstitution {
        substitute(module("io.github.pehoeji:konvert-legacy-poj")).using(project(":"))
    }
}
includeBuild("KonvertToPOJ") {
    dependencySubstitution {
        substitute(module("tw.poj.kesi:konvert-to-poj")).using(project(":lib"))
    }
}

include(":pipeline")
