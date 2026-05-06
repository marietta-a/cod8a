using CodeAnalyzer.models;
using Microsoft.CodeAnalysis;
using Microsoft.CodeAnalysis.CSharp;
using Microsoft.CodeAnalysis.CSharp.Syntax;
using System;
using System.Collections.Generic;
using System.Text;

namespace CodeAnalyzer.Parsers
{
    public sealed partial class ProjectParser<T> : BaseParser<T> where T : ProjectStructure
    {
        public override string Name { get; init; }
        
        public string[] FilePaths { get; init; }

        public override T Parse()
        {
            try
            {
                var projectStructure = new ProjectStructure
                {
                    Id = 1,
                    Name = Name,
                    Files = FilePaths.Select(b => new FileParser<FileStructure> { FilePath = b, Name = Path.GetFileName(b) }.Parse()).ToList(),
                };
                
                return (T) projectStructure;
            }
            catch (Exception ex)
            {
                throw;
            }
        }
    }

}