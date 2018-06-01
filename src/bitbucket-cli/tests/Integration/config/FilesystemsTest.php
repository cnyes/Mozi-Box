<?php

namespace Tests\Unit;

use Tests\TestCase;

class FilesystemsTest extends TestCase
{
    public function testConfig()
    {
        putenv("APP_TMP_DIR");

        $this->initialApplication();

        $this->assertEquals(
            ["driver" => "local", "root" => env("HOME") . DIRECTORY_SEPARATOR . ".cnyesDeploymentCli.d"],
            config("filesystems.disks.app_local")
        );
    }

    public function testConfigWithEnv()
    {
        putenv("APP_TMP_DIR=/tmp");

        $this->initialApplication();

        $this->assertEquals(["driver" => "local", "root" => "/tmp"], config("filesystems.disks.app_local"));
    }
}
