using System;
using System.Collections.Generic;
using System.Text;

namespace CodeAnalyzer.models
{
    public  class SolutionStructure
    {
        /// <summary>
        /// Gets or sets the ID of the Solution
        /// </summary>
        public int Id { get; set; }
        /// <summary>
        /// Gets or sets the name of the Solution
        /// </summary>
        public string Name { get; set; }

        /// <summary>
        /// Gets or sets the description associated with the object.
        /// </summary>
        public string Description { get; set; }

        /// <summary>
        /// Gets or sets the collection of projects within this solution
        /// </summary>
        public List<ProjectStructure> Projects { get; set; }
    }
}
