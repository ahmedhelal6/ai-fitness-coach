using Ai_Fitness_Coach.Data;
using Ai_Fitness_Coach.DTOs;
using Ai_Fitness_Coach.Models;
using Microsoft.EntityFrameworkCore;

namespace Ai_Fitness_Coach.Services
{
    public class WorkoutService : IWorkoutService
    {
        private readonly ApplicationDbContext _context;
        public WorkoutService(ApplicationDbContext context)
        {
            _context = context;
        }
        public async Task<WorkoutSession> StartWorkoutAsync(int userId, StartWorkoutRequest request)
        {
            var session = new WorkoutSession
            {
                UserId = userId,
                StartTime = DateTime.UtcNow,
                Notes = request.Notes ?? ""
            };

            _context.WorkoutSessions.Add(session);
            await _context.SaveChangesAsync();

            return session;
        }
        public async Task EndWorkoutAsync(int userId, int sessionId)
        {
            var session = await _context.WorkoutSessions
                .FirstOrDefaultAsync(s => s.Id == sessionId && s.UserId == userId)
                ?? throw new Exception("Session not found");

            session.EndTime = DateTime.UtcNow;
            // Total Reps
            int totalReps = session.WorkoutSets.Sum(s => s.Reps);
            //totalVolume
            double totalVolume = session.WorkoutSets
                .Sum(s => s.Weight.HasValue ? (double)(s.Weight.Value * s.Reps) : 0);
            //model shit
            double? avgFormScore = null;

            if (session.ExerciseAnalyses.Any())
            {
                avgFormScore = session.ExerciseAnalyses
                    .Average(a => a.FormScore);
            }
            string summary = GenerateSummary(totalReps, totalVolume, avgFormScore);
            var analysis = new WorkoutAnalysis
            {
                SessionId = session.Id,
                TotalReps = totalReps,
                TotalVolume = totalVolume,
                AvgFormScore = avgFormScore,
                Summary = summary,
                CreatedAt = DateTime.UtcNow
            };
            _context.WorkoutAnalyses.Add(analysis);
            await _context.SaveChangesAsync();

        }
        public async Task AddSetAsync(int userId, AddSetRequest request)
        {
            var session = await _context.WorkoutSessions
                .FirstOrDefaultAsync(s => s.Id == request.WorkoutSessionId && s.UserId == userId)
                ?? throw new Exception("Session not found");

            var setCount = await _context.WorkoutSets
                .CountAsync(s => s.WorkoutSessionId == request.WorkoutSessionId);

            var set = new WorkoutSet
            {
                WorkoutSessionId = request.WorkoutSessionId,
                ExerciseId = request.ExerciseId,
                Reps = request.Reps,
                Weight = request.Weight,
                SetNumber = setCount + 1
            };

            _context.WorkoutSets.Add(set);
            await _context.SaveChangesAsync();
        }
        public async Task<List<WorkoutSession>> GetUserWorkoutsAsync(int userId)
        {
            return await _context.WorkoutSessions
                .Where(w => w.UserId == userId)
                .Include(w => w.WorkoutSets)
                    .ThenInclude(ws => ws.Exercise)
                .Include(w => w.User)
                .OrderByDescending(w => w.StartTime)
                .ToListAsync();
        }
        public async Task<List<WorkoutSet>> GetSessionSetsAsync(int sessionId)
        {
            return await _context.WorkoutSets
                .Where(s => s.WorkoutSessionId == sessionId)
                .Include(s => s.Exercise)
                .ToListAsync();
        }
        private string GenerateSummary(int totalReps, double totalVolume, double? avgFormScore)
        {
            if (totalReps == 0)
                return "No workout data recorded.";

            string baseSummary = $"You completed {totalReps} reps with a total volume of {totalVolume:F1}.";

            if (avgFormScore.HasValue)
            {
                string performance = avgFormScore.Value switch
                {
                    >= 85 => " Excellent form!",
                    >= 70 => " Good form overall.",
                    >= 50 => " Needs improvement.",
                    _ => " Poor form."
                };

                return baseSummary + performance;
            }

            return baseSummary + " No form analysis available.";
        }
    }
}
