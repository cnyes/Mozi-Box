<?php

namespace Tests\Unit;

use App\Commands\Bitbucket\PatchDiffCommand;
use App\Support\Facades\AppStorage;
use App\Support\Facades\Bitbucket;
use App\Support\Facades\GitClient;
use Tests\TestCase;

class PatchDiffCommandTest extends TestCase
{
    public function testHandle(): void
    {
        AppStorage::shouldReceive("putTmp")->once()->andReturn(true);
        AppStorage::shouldReceive("deleteTmp")->once()->andReturn(true);
        Bitbucket::shouldReceive("getDiffByProjectAndPullRequestId")->once()->andReturn("");
        GitClient::shouldReceive("applyDiff")->once()->andReturn(true);

        $command = new PatchDiffCommand();
        $this->app->call($command->getName(), ['id' => [9999], 'project' => 'test']);

        $this->assertEquals($this->app->output(), "fetch diff file By PR. Id = 9999\nbegin to apply diff file.\n");
    }
}
