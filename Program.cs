using CSnakes.Runtime;
using CSnakes.Runtime.Python;

var builder = WebApplication.CreateBuilder(args);



// Add services to the container.
// Learn more about configuring OpenAPI at https://aka.ms/aspnet/openapi
builder.Services.AddOpenApi();
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();


string home = Path.Join(Environment.CurrentDirectory, "./python");

builder.Services.WithPython()
    .FromRedistributable()
    .WithHome(home)
    .WithPipInstaller()
    .WithVirtualEnvironment(Path.Join(home, "venv"));


builder.Services.AddSingleton(x => x.GetRequiredService<IPythonEnvironment>().ChromaDb());

var app = builder.Build();

// Configure the HTTP request pipeline.
if (app.Environment.IsDevelopment())
{
    app.MapOpenApi();
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseHttpsRedirection();


app.MapPost("/chromadb/add", (IChromaDb chromaDb, string text) =>
{
    chromaDb.AddText(PyObject.From(text));
    return Results.Ok();
}).WithName("AddText");

app.MapPost("/chromadb/search", (IChromaDb chromaDb, string query) =>
{
    var results = chromaDb.SearchText(PyObject.From(query));
    return Results.Ok(results);
}).WithName("SearchText");


app.Run();

record WeatherForecast(DateOnly Date, int TemperatureC, string? Summary)
{
    public int TemperatureF => 32 + (int)(TemperatureC / 0.5556);
}
