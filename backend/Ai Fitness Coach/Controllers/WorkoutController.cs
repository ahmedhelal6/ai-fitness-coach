using Ai_Fitness_Coach.DTOs;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using System.Security.Claims;

namespace Ai_Fitness_Coach.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    [Authorize]
    public class WorkoutController : ControllerBase
    {
        private readonly IWorkoutService _service;

        public WorkoutController(IWorkoutService service)
        {
            _service = service;
        }

        private int GetUserId()
        {
            return int.Parse(User.FindFirst(ClaimTypes.NameIdentifier)!.Value);
        }

        [HttpPost("start")]
        public async Task<IActionResult> StartWorkout(StartWorkoutRequest request)
        {
            var userId = GetUserId();
            var session = await _service.StartWorkoutAsync(userId, request);
            return Ok(session);
        }

        [HttpPost("end")]
        public async Task<IActionResult> EndWorkout(EndWorkoutRequest request)
        {
            var userId = GetUserId();
            await _service.EndWorkoutAsync(userId, request.SessionId);
            return Ok(new { message = "Workout ended" });
        }

        [HttpPost("set")]
        public async Task<IActionResult> AddSet(AddSetRequest request)
        {
            var userId = GetUserId();
            await _service.AddSetAsync(userId, request);
            return Ok(new { message = "Set added" });
        }

        [HttpGet]
        public async Task<IActionResult> GetUserWorkouts()
        {
            var userId = GetUserId();
            var workouts = await _service.GetUserWorkoutsAsync(userId);
            return Ok(workouts);
        }

        [HttpGet("{sessionId}/sets")]
        public async Task<IActionResult> GetSessionSets(int sessionId)
        {
            var sets = await _service.GetSessionSetsAsync(sessionId);
            return Ok(sets);
        }
    }
}
