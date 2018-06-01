<?php

namespace Tests\Unit;

use App\Services\Bitbucket\ApiService;
use Bitbucket\API\Repositories\PullRequests;
use Buzz\Message\MessageInterface;
use Mockery as m;
use Tests\TestCase;

class ApiServiceTest extends TestCase
{
    public function testGetDiffByProjectAndPullRequestId()
    {
        $pull = m::mock(PullRequests::class);
        $message = m::mock(MessageInterface::class);

        $team = "test_team";
        $project = "test_project";
        $pullRequest = "9999";
        $returnMessage = "Hello! Go Diff";

        $pull->shouldReceive("diff")->with($team, $project, $pullRequest)->once()->andReturn($message);
        $message->shouldReceive("getContent")->once()->andReturn("Hello! Go Diff");

        $client = new ApiService($pull, $team);
        $diff = $client->getDiffByProjectAndPullRequestId($project, $pullRequest);
        $this->assertEquals($diff, $returnMessage);
    }
}
