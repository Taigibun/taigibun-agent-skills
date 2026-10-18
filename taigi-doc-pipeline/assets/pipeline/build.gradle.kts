plugins {
    kotlin("jvm") version "2.2.21"
    application
}

repositories {
    mavenCentral()
}

dependencies {
    implementation("io.github.pehoeji:konvert-legacy-poj:0.1.0")
    implementation("tw.poj.kesi:konvert-to-poj:0.6.0")
}

kotlin {
    jvmToolchain(17)
}

application {
    mainClass.set("taibun.pipeline.PipelineFixKt")
}
