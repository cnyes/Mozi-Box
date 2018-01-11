<?php

namespace Tests\Unit;

use App\Foundation\Git\GitRepository;
use Cz\Git\GitException;
use Cz\Git\GitRepository as BaseGitRepository;
use Mockery as m;
use phpmock\mockery\PHPMockery as mm;
use Tests\TestCase;

class GitRepositoryTest extends TestCase
{
    public function testApplyDiff()
    {
        $diffFilePath = "/tmp/patch.diff";

        mm::mock("\App\Foundation\Git", "file_exists")->once()->andReturn(true);
        mm::mock("\App\Foundation\Git", "realpath")->once()->andReturn($diffFilePath);

        $gitRepository = m::mock(GitRepository::class)->makePartial()->shouldAllowMockingProtectedMethods();
        $gitRepository->shouldReceive("begin")->once()->andReturnSelf();
        $gitRepository->shouldReceive("end")->once()->andReturnSelf();
        $gitRepository->shouldReceive("run")->with("git apply", $diffFilePath)->once()->andReturnSelf();

        $return = $gitRepository->applyDiff($diffFilePath);
        $this->assertInstanceOf(BaseGitRepository::class, $return);
    }

    public function testApplyDiffWithException()
    {
        $diffFilePath = "/tmp/patch.diff";

        mm::mock("\App\Foundation\Git", "file_exists")->once()->andReturn(true);
        mm::mock("\App\Foundation\Git", "realpath")->once()->andReturn($diffFilePath);

        $gitRepository = m::mock(GitRepository::class)->makePartial()->shouldAllowMockingProtectedMethods();
        $gitRepository->shouldReceive("begin")->once()->andReturnSelf();
        $gitRepository->shouldReceive("end")->times(0);

        $gitRepository
            ->shouldReceive("run")
            ->with("git apply", $diffFilePath)
            ->once()
            ->andThrow(new GitException("error"));

        $this->expectException(GitException::class);
        $this->expectExceptionMessage("git apply failed.");

        $return = $gitRepository->applyDiff($diffFilePath);
    }

    public function testCheckBeforeApplyDiff()
    {
        $diffFilePath = "/tmp/patch.diff";

        mm::mock("\App\Foundation\Git", "file_exists")->once()->andReturn(true);
        mm::mock("\App\Foundation\Git", "realpath")->once()->andReturn($diffFilePath);

        $gitRepository = m::mock(GitRepository::class)->makePartial()->shouldAllowMockingProtectedMethods();
        $gitRepository->shouldReceive("begin")->once()->andReturnSelf();
        $gitRepository->shouldReceive("end")->once()->andReturnSelf();
        $gitRepository->shouldReceive("run")->with("git apply", "--check", $diffFilePath)->once()->andReturnSelf();

        $return = $gitRepository->checkBeforeApplyDiff($diffFilePath);
        $this->assertInstanceOf(BaseGitRepository::class, $return);
    }

    public function testCheckBeforeApplyDiffWithException()
    {
        $diffFilePath = "/tmp/patch.diff";

        mm::mock("\App\Foundation\Git", "file_exists")->once()->andReturn(true);
        mm::mock("\App\Foundation\Git", "realpath")->once()->andReturn($diffFilePath);

        $gitRepository = m::mock(GitRepository::class)->makePartial()->shouldAllowMockingProtectedMethods();
        $gitRepository->shouldReceive("begin")->once()->andReturnSelf();
        $gitRepository->shouldReceive("end")->times(0);

        $gitRepository
            ->shouldReceive("run")
            ->with("git apply", "--check", $diffFilePath)
            ->once()
            ->andThrow(new GitException("error"));

        $this->expectException(GitException::class);
        $this->expectExceptionMessage("git apply check failed.");

        $return = $gitRepository->checkBeforeApplyDiff($diffFilePath);
    }

    public function testCheckFileExists()
    {
        $diffFilePath = "/tmp/patch.diff";

        mm::mock("\App\Foundation\Git", "file_exists")->once()->andReturn(true);
        mm::mock("\App\Foundation\Git", "realpath")->once()->andReturn($diffFilePath);

        $gitRepository = m::mock(GitRepository::class)->makePartial();
        $path = $gitRepository->checkFileExists($diffFilePath);
        $this->assertEquals($path, $diffFilePath);
    }

    public function testCheckFileExistsWithException()
    {
        $diffFilePath = "/tmp/patch.diff";

        mm::mock("\App\Foundation\Git", "file_exists")->once()->andReturn(false);
        $gitRepository = m::mock(GitRepository::class)->makePartial();

        $this->expectException(GitException::class);
        $this->expectExceptionMessage("diff path file is not exists.");

        $path = $gitRepository->checkFileExists($diffFilePath);
    }
}
