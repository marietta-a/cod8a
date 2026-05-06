using CodeAnalyzer.models;
using System;
using System.Collections.Generic;
using System.Text;

namespace CodeAnalyzer.Parsers
{
    public sealed partial class SolutionParser<T> : BaseParser<T> where T : SolutionStructure
    {
        public override string Name { get; init; }

        public override T Parse()
        {
            throw new NotImplementedException();
        }
    }
}
