<?php

namespace Tests\Unit;

use Tests\TestCase;

class HelperTest extends TestCase
{
    public function testAppLocalPathWithOutEnv(): void
    {
        putenv("APP_TMP_DIR");

        $this->initialApplication();

        $path = app_local_path();
        $this->assertEquals($path, join_path([env("HOME"), ".cnyesDeploymentCli.d"]));

        $path = app_local_path("application");
        $this->assertEquals($path, join_path([env("HOME"), ".cnyesDeploymentCli.d", "application"]));
    }

    public function testAppLocalPathWithEnv(): void
    {
        $tmpDir = "/tmp_application/dir";
        putenv("APP_TMP_DIR=$tmpDir");

        $this->initialApplication();

        $path = app_local_path();
        $this->assertEquals($path, $tmpDir);

        $path = app_local_path("application");
        $this->assertEquals($path, join_path([$tmpDir, "application"]));
    }

    public function testAppLocalTmpPathWithOutEnv(): void
    {
        putenv("APP_TMP_DIR");

        $this->initialApplication();

        $path = app_local_tmp_path();
        $this->assertEquals($path, join_path([env("HOME"), ".cnyesDeploymentCli.d", "tmp"]));

        $path = app_local_tmp_path("application");
        $this->assertEquals($path, join_path([env("HOME"), ".cnyesDeploymentCli.d", "tmp", "application"]));
    }

    public function testAppLocalTmpPathWithEnv(): void
    {
        $tmpDir = "/tmp_application/dir";
        putenv("APP_TMP_DIR=$tmpDir");

        $this->initialApplication();

        $path = app_local_tmp_path();
        $this->assertEquals($path, join_path([$tmpDir, "tmp"]));

        $path = app_local_tmp_path("application");
        $this->assertEquals($path, join_path([$tmpDir, "tmp", "application"]));
    }

    public function testJoinPath(): void
    {
        $this->assertEquals(
            join_path(["/tmp", "aaa", "bbb"]),
            "/tmp" . DIRECTORY_SEPARATOR . "aaa" . DIRECTORY_SEPARATOR . "bbb"
        );
    }
}
