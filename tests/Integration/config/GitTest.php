<?php

namespace Tests\Unit;

use Tests\TestCase;

class GitTest extends TestCase
{
    public function testConfig()
    {
        putenv("GIT_REPOSITORY_PATH");

        $this->initialApplication();

        $this->assertEquals(null, config('git.repository_path'));
    }

    public function testConfigWithEnv()
    {
        putenv("GIT_REPOSITORY_PATH=/tmp/git_repository");

        $this->initialApplication();

        $this->assertEquals('/tmp/git_repository', config('git.repository_path'));
    }
}
