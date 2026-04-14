using Ai_Fitness_Coach.DTOs;
using Ai_Fitness_Coach.Models;

public interface IWorkoutService
{
    Task<WorkoutSession> StartWorkoutAsync(int userId, StartWorkoutRequest request);
    Task EndWorkoutAsync(int userId, int sessionId);
    Task AddSetAsync(int userId, AddSetRequest request);
    Task<List<WorkoutSession>> GetUserWorkoutsAsync(int userId);
    Task<List<WorkoutSet>> GetSessionSetsAsync(int sessionId);
}