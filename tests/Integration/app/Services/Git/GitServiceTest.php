<?php

namespace Tests\Unit;

use App\Foundation\Git\GitRepository;
use App\Services\Git\GitService;
use Mockery as m;
use Tests\TestCase;

class GitServiceTest extends TestCase
{
    public function testApplyDiff()
    {
        $gitRepository = m::mock(GitRepository::class);

        $diffFilePath = "/tmp/patch.diff";

        $gitRepository->shouldReceive("applyDiff")->with($diffFilePath)->once()->andReturnSelf();
        $gitRepository->shouldReceive("checkBeforeApplyDiff")->with($diffFilePath)->once()->andReturnSelf();

        $client = new GitService($gitRepository);
        $return = $client->applyDiff($diffFilePath);
        $this->assertEquals(true, $return);
    }
}
