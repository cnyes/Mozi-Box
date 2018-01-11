<?php

namespace Tests\Unit;

use Tests\TestCase;

class BitbucketTest extends TestCase
{
    public function testConfig()
    {
        putenv("BITBUCKET_ID");
        putenv("BITBUCKET_SECRET");
        putenv("BITBUCKET_TEAM");

        $this->initialApplication();

        $this->assertEquals('test_id', config('bitbucket.id'));
        $this->assertEquals('test_secret', config('bitbucket.secret'));
        $this->assertEquals('test_team', config('bitbucket.team'));
    }

    public function testConfigWithEnv()
    {
        putenv("BITBUCKET_ID=go_id");
        putenv("BITBUCKET_SECRET=go_secret");
        putenv("BITBUCKET_TEAM=go_team");

        $this->initialApplication();

        $this->assertEquals('go_id', config('bitbucket.id'));
        $this->assertEquals('go_secret', config('bitbucket.secret'));
        $this->assertEquals('go_team', config('bitbucket.team'));
    }
}
